from email.policy import default
from unicodedata import category
from sqlalchemy import Column, ForeignKey
from nautilus import app,db,login_manager
from flask_migrate import Migrate
from datetime import datetime, timezone
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer,SignatureExpired

s=URLSafeTimedSerializer('hgcgyctdcbchhbx')

heading_child1=db.Table('heading_child1',
    db.Column('child1_id',db.Integer,db.ForeignKey('child1.id'),primary_key=True),
    db.Column('heading_id',db.Integer,db.ForeignKey('heading.id'),primary_key=True)
)
parent_heading=db.Table('parent_heading',
    db.Column('heading_id',db.Integer,db.ForeignKey('heading.id'),primary_key=True),
    db.Column('parent_id',db.Integer,db.ForeignKey('parent.id'),primary_key=True)
)
class Parent(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.Text,nullable=False)
    select=db.Column(db.Boolean(),default=False)
    heading=db.relationship('Heading',secondary=parent_heading,back_populates='parent')

    def __repr__(self):
        return self.question

class Heading(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    heading=db.Column(db.Text,nullable=False)
    child1=db.relationship('Child1',secondary=heading_child1,back_populates='heading')
    parent=db.relationship('Parent',secondary=parent_heading,back_populates='heading')

    def __repr__(self):
            return F"{self.heading} selections:{self.child1}"
class Child1(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.Text,nullable=False)
    page_summary=db.Column(db.Text,nullable=True,default='hi')
    mail_response=db.Column(db.Text,nullable=True,default='hi')
    heading=db.relationship('Heading',secondary=heading_child1,back_populates='child1')
    def __repr__(self):
            return self.question



class ConfirmUser(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(50))
    last_name=db.Column(db.String(50))
    company_email=db.Column(db.String(50))
    company_name=db.Column(db.String(50))
    company_region=db.Column(db.String(50))
    confirmed=db.Column(db.Boolean, default=False, nullable=True)
    
    def __repr__(self):
        return f"{self.id}-{self.first_name}"
    def get_verify_email_token(self):
        return s.dumps({'user_id':self.company_email},salt='confirm_email')
    @staticmethod
    def verify_email_token(token):
        try:  
            user_id = s.loads(token,salt='confirm_email',max_age=200)
        except SignatureExpired:
            return None
        user=user_id['user_id']
        return user
  
@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))      
class AdminUser(db.Model,UserMixin):
    __table_args__ = {'extend_existing': True}
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    password1=db.Column(db.Text())
    password2=db.Column(db.Text())
    permission=db.Column(db.Boolean, default=False, nullable=True)
    super_permission=db.Column(db.Boolean, default=False, nullable=True)
   
    
    
class Tree(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.Text,nullable=True)
    answer=db.Column(db.Text,nullable=True)
    answer1=db.relationship('Branch1',backref='tree',cascade='all,delete',lazy=True)

    def __repr__(self):
        return f"{self.id}-{self.question}"



class Branch1(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.Text,nullable=True)
    answer=db.Column(db.Text,nullable=True)
    tree_id=db.Column(db.Integer,db.ForeignKey('tree.id'),nullable='False')
    branch2=db.relationship('Branch2',backref='branch1',cascade='all,delete',lazy=True)

    def __repr__(self):
        return f"{self.id}-{self.question}-{self.tree.id}-{self.tree.question}"

class Branch2(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.Text,nullable=True)
    answer=db.Column(db.Text,nullable=True)
    branch1_id=db.Column(db.Integer,db.ForeignKey('branch1.id'),nullable='False')
    answer=db.relationship('Answer',backref='branch2',cascade='all,delete',lazy=True)

    def __repr__(self):
        return f"{self.id}-{self.question}-{self.branch1.id}-{self.branch1.question}"
class Answer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.Text,nullable=True)
    page_summary=db.Column(db.Text,nullable=True,default='hi')
    mail_response=db.Column(db.Text,nullable=True,default='hi')
    branch2_id=db.Column(db.Integer,db.ForeignKey('branch2.id'),nullable='False')
    def __repr__(self):
        return f"{self.id}-{self.page_summary}"