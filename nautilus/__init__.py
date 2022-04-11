from distutils import bcppcompiler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://owrqilwwyfvgiz:8e03610d36b446d1424950d997496f8ecb5569d415cbbc049c85d9bdca81807a@ec2-3-217-251-77.compute-1.amazonaws.com:5432/d6a7gbqujadb5d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY']='shfrfkenvrdgdg6djjguigv@ft'
db=SQLAlchemy(app)
migrate=Migrate(app,db)
mail=Mail(app)
bcrypt=Bcrypt(app)

# login_manager = LoginManager(app)
# login_manager.init_app(app)


from . import app
