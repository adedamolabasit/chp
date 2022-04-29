from distutils import bcppcompiler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wtzyegodvafvqe:5592a0206fd4d997420f01e6201a345567756caea4f66488cec2381671be061a@ec2-3-212-45-192.compute-1.amazonaws.com:5432/d2ap268nr1oibk'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yourusername:yourpassword@localhost:5432/yourdatabasename'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY']='shfrfkhhenvrdgdg6djjguigv@ft'
db=SQLAlchemy(app)
migrate=Migrate(app,db)
mail=Mail(app)
bcrypt=Bcrypt(app)

app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME']="cloudhelpprovider@gmail.com"
app.config['MAIL_PASSWORD']="@@Health2020"





db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)


from . import app
