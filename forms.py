# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import BooleanField,TextAreaField,PasswordField,SubmitField,StringField,SelectMultipleField
from wtforms.validators import DataRequired,Length,EqualTo
from wtforms import widgets
from models import User

class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators=[Length(min=6, max=35)])
    password = PasswordField(u'密码',validators=[DataRequired()])
    remember_me = BooleanField(u'记住密码', default=False)
    submit = SubmitField(u'提交')

class RegisterForm(FlaskForm):
    nickname = StringField(u'昵称', validators= [Length(min=4, max=25)])
    password = PasswordField(u'密码',
        validators = [DataRequired(),EqualTo('confirm', message='Passwords must match')],)
    confirm = PasswordField(u'确认密码')
    email = StringField(u'邮箱', validators = [Length(min=6, max=35)])
    submit = SubmitField(u'提交')

class CommentForm(FlaskForm):
    post = TextAreaField(u'评论', validators = [DataRequired()])
    submit = SubmitField(u'提交')

class SearchForm(FlaskForm):
    content = StringField(u'content', validators = [DataRequired()])
    submit = SubmitField(u'提交')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

my_choices = [('1', '2016'), ('2', '2015')]
class YearForm(FlaskForm):
    year = SelectMultipleField(label='year',choices=my_choices,
                                validators = [DataRequired()])
    month = SelectMultipleField(label='year', choices=my_choices,
                              validators=[DataRequired()])

    submit1 = SubmitField(u'提交')

