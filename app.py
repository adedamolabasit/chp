from itertools import product
from locale import currency
from flask import render_template,session,request,redirect,url_for,flash,g
from nautilus import app,db,mail,bcrypt
from flask_admin import Admin
from nautilus.models import *
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import secure_filename
from PIL import Image
import os
from datetime import date
from werkzeug.utils import secure_filename
from sqlalchemy import desc 
import os
from flask_login import current_user, fresh_login_required,login_user,logout_user,login_required
from nautilus import *
from flask_mail import Message
import secrets
import stripe
import re
from jinja2 import evalcontextfilter
from markupsafe import Markup, escape

@app.route('/')
def index():
    return('hello world')




if __name__ == "__main__":
    app.run(debug=True)
