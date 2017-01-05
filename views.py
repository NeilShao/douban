# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from douban import cursor
from forms import LoginForm,RegisterForm,CommentForm,SearchForm,YearForm
from models import User,Comment
from douban import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from douban.config import POSTS_PER_PAGE

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
def index(page = 1):
    page_now = page
    query_sql = "select image,title,rate,id from movie where rating_people>100000 order by YEAR  and  RATE  desc"
    cursor.execute(query_sql)
    while page != 0:
        movies = cursor.fetchmany(16)
        page = page - 1
        if len(movies) < 1:
            page = -1
    g.search_form = SearchForm(request.form)
    if g.search_form.validate_on_submit():

        content = g.search_form.content.data
        print content
        return redirect(url_for('search', content = content))

    year_form = YearForm(request.form)

    return render_template('index.html',movies = movies,page = page_now,search_form = g.search_form,
                           year_form = year_form)

@app.route('/search', methods = ['GET', 'POST'])
@app.route('/search/<int:page>', methods = ['GET', 'POST'])
def search(page = 1,content = '*'):
    over = 0
    if request.args.get('content'):
        content = request.args.get('content')

    page_now = page
    query_sql = "select image,title,rate,id from movie where title LIKE '%{0}%' ORDER BY rate DESC ".format(content)
    print query_sql
    cursor.execute(query_sql)
    while page != 0:
        movies = cursor.fetchmany(16)

        page = page - 1
        if len(movies) < 16:
            over = 1
    if g.search_form.validate_on_submit():
        return redirect(url_for('search', content=g.search_form.content.data))
    return render_template('search.html', movies=movies, page=page_now,search_form=g.search_form,over = over,content=content)

@app.route('/subject/<int:id>', methods = ['GET', 'POST'])
@app.route('/subject/<int:id>/<int:page>', methods = ['GET', 'POST'])
@login_required
def subject(id = 35,page = 1):
    form = CommentForm()
    query_sql = "select * from movie WHERE id=%d" %(id)
    cursor.execute(query_sql)
    movie = cursor.fetchone()
    comments = Comment.query.filter(Comment.movie_id == id).order_by(Comment.timestamp.desc()).\
        paginate(page, POSTS_PER_PAGE, False)

    if request.method == 'POST' and form.validate_on_submit():
        if len(form.post.data) > 140:
            return render_template('subject.html', movie=movie,
                                   comments=comments, form=form)
        movie_name = movie[2].split(' ')[0]
        comment = Comment(body=form.post.data, timestamp=datetime.utcnow(), author=g.user, movie_id=id,movie_name=movie_name)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('subject',id = id,page = page))
    return render_template('subject.html',movie = movie,
                           comments = comments,form = form)

@app.route('/friend/<int:id>', methods = ['GET', 'POST'])
@app.route('/friend/<int:id>/<int:page>', methods = ['GET', 'POST'])
@login_required
def friend(id = 35,page = 1):
    form = CommentForm()
    query_sql = "select * from movie WHERE id=%d" %(id)
    cursor.execute(query_sql)
    movie = cursor.fetchone()
    comments = g.user.followed_comments().filter(Comment.movie_id == id).paginate(page, POSTS_PER_PAGE, False)

    if request.method == 'POST' and form.validate_on_submit():
        if len(form.post.data) > 140:
            return render_template('friend.html', movie=movie,
                                   comments=comments, form=form)
        movie_name = movie[2].split(' ')[0]
        comment = Comment(body=form.post.data, timestamp=datetime.utcnow(), author=g.user, movie_id=id,movie_name=movie_name)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('friend', id=id))

    return render_template('friend.html',movie = movie,
                           comments = comments,form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    #if g.user is not None and g.user.is_authenticated:
    #    return redirect(url_for('index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('邮箱或密码错误', 'danger')

    return render_template('login.html',
                        title=u'登陆',form = form)

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        nickname = User.query.filter_by(email=form.nickname.data).first()
        if email is None and nickname is None:
            User.insert_admin(form.email.data,form.nickname.data,form.password.data)
            return redirect(url_for('login'))
        else:
            flash('The nickname or email is exist')

    return render_template('register.html',
                           title=u'注册',form=form)

@app.route('/user/<nickname>',methods=['GET', 'POST'])
@login_required
def user(nickname,page = 1,friend_page = 1,friend = 0):
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('friend_page'):
        friend_page = int(request.args.get('friend_page'))
    if request.args.get('friend'):
        friend = int(request.args.get('friend'))

    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('No User:' + nickname + '!')
        return redirect(url_for('index'))
    comments = user.comments.order_by(Comment.timestamp.desc()).paginate(page,POSTS_PER_PAGE, False)
    comments_friends = user.followed_comments().paginate(friend_page,POSTS_PER_PAGE, False)

    return render_template('user.html',
        user = user,comments = comments,comments_friends = comments_friends,friend = friend)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '!')
    return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))


