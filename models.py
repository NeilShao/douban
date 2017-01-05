# -*- coding:utf-8 -*-
from douban import db
from werkzeug.security import generate_password_hash, check_password_hash
import random

ROLE_USER = 0
ROLE_ADMIN = 1

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique= True)
    email = db.Column(db.String(120), index = True, unique =  True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    comments = db.relationship('Comment',backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
    password_hash = db.Column(db.String(128))

    @staticmethod
    def insert_admin(email, nickname, password):
        user = User(email=email, nickname=nickname, password=password)
        db.session.add(user)
        db.session.commit()
        db.session.add(user.follow(user))
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_comments(self):
        return Comment.query.join(followers, (followers.c.followed_id == Comment.user_id)).filter(
            followers.c.follower_id == self.id).order_by(Comment.timestamp.desc())

    @staticmethod
    def make_unique_nickname(nickname):
        new_nickname = ""
        if User.query.filter_by(nickname=nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() == None:
                break
            version += 1
        return new_nickname

    def avatar(self, size):
        return "http://p1.qqyou.com/touxiang/UploadPic/2015-6/19/2015061914565043612.jpeg"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    movie_id = db.Column(db.String(140))
    movie_name = db.Column(db.String(140))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer,db.ForeignKey(User.id))

    def get_comment(self,movie_id):
        return Comment.query.filter(movie_id = movie_id).order_by(Comment.timestamp.desc())

    def __repr__(self):
        return '<Comment %r>' % (self.body)