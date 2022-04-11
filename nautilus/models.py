from unicodedata import category
from sqlalchemy import Column
from nautilus import app,db
from flask_migrate import Migrate
from datetime import datetime, timezone
from flask_login import UserMixin