from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import length,DataRequired,Email,EqualTo,ValidationError
from .models import AdminUser

class LoginForm(FlaskForm):
    
     email=StringField('Email',validators=[DataRequired(),Email()],render_kw={'placeholder':'Email'})
     password=PasswordField('Password',validators=[DataRequired()],render_kw={'placeholder':'password'}) 
     submit=SubmitField('Login')
     def user(self,email):
         exusting_user=AdminUser.query.filter_by(email=email).first()
         if not exusting_user:
             raise ValidationError(f'You are not an Admin')
     

class RegistrationForm(FlaskForm):
     email=StringField('Email',validators=[DataRequired(),Email()],render_kw={'placeholder':'Email'})  
     password=PasswordField('Password',validators=[DataRequired()],render_kw={'placeholder':'************'})   
     confirm_password=PasswordField('Confirm password',validators=[DataRequired(),EqualTo('password')],render_kw={'placeholder':'************'})   
     submit=SubmitField('Register')
     def validate_email(self,email):
            existing_email=AdminUser.query.filter_by(email=email.data).first()
            if existing_email:
                raise ValidationError(f"This Email is already registered to Nautius Admin , navigate to Sign In to have access to the Adminpage")