from flask import Flask
from config import basedir
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import MySQLdb

app = Flask(__name__)
app.config.from_pyfile('config.py')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

movie_db = MySQLdb.connect("localhost", "root", "950520", "douban",charset="utf8")
cursor = movie_db.cursor()

import views,models






