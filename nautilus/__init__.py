from distutils import bcppcompiler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qhytskhqxcjpit:6f92d94296ca49b3ecb98f97164c05ad3e5d268c7684bed1650225c258d8c960@ec2-34-192-210-139.compute-1.amazonaws.com:5432/d96kl0p70jcngg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY']='shfrfkenvrdgdg6djjguigv@ft'
db=SQLAlchemy(app)
migrate=Migrate(app,db)
mail=Mail(app)
bcrypt=Bcrypt(app)

app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
# app.config['MAIL_USERNAME']="adedamolabasit09@gmail.com"
# app.config['MAIL_PASSWORD']="Nautilus6he!"
app.config['MAIL_USERNAME']="cloudhelpprovider@gmail.com"
app.config['MAIL_PASSWORD']="@@Health2020"





db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)


from . import app
