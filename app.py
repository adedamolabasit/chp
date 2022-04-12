from itertools import product
from locale import currency
from flask import render_template,session,request,redirect,url_for,flash,g,abort
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
from nautilus.forms import *
from flask_mail import Message
import secrets
import stripe
import re
from jinja2 import evalcontextfilter
from markupsafe import Markup, escape

admin=Admin(app,template_mode='bootstrap3',name='Nautilus Admin')

class Controllers(ModelView):
    pass
    # def is_accessible(self):

    #     if current_user.is_active:
    #         if current_user.permission is True:
    #             return current_user.is_authenticated 
    #         else:
    #             abort(403)           
    #     else: 
    #         abort(403)
    
   
 

    # def not_auth(self):
    #     return " you are not authorized to use the Nautilus dashboard "

admin.add_view(Controllers(Parent,db.session,name='what is critical to your organization when migrating to cloud'))
admin.add_view(Controllers(Heading,db.session,name='Heading'))
admin.add_view(Controllers(Child1,db.session,name='child'))
# admin
admin.add_view(Controllers(Tree,db.session,name='First Question'))
admin.add_view(Controllers(Branch1,db.session,name='Second Question'))
admin.add_view(Controllers(Branch2,db.session,name='Third Question'))
admin.add_view(Controllers(Answer,db.session,name='Summary and Email body'))
admin.add_view(Controllers(ConfirmUser,db.session,name='Email Collections'))
admin.add_view(Controllers(AdminUser,db.session,name='Nautilus Admin'))

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/prompt')
def prompt():
    return render_template('prompt.html')
@app.route('/chp1')
def parent():
    query=Parent.query.order_by(Parent.id).all()
    return render_template('parent.html',query=query)
@app.route('/options',methods=["POST"])
def child1():
    options=request.form.getlist('check')
    headings=Heading.query.join(Heading.parent).filter(Parent.id.in_(options)).first()
    return render_template('child1.html',headings=headings)

@app.route('/report/<int:id>')
def report(id):
    query=Child1.query.filter_by(id=id).first()
    if query is None:
        abort(404)
    return render_template('summary.html',query=query)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
# config


# admin



@app.route('/nautilus-admin/sign-in',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        form=LoginForm()
        if form.validate_on_submit():
            email=form.email.data
            user=AdminUser.query.filter_by(email=email).first()
            if user:
                if bcrypt.check_password_hash(user.password1,form.password.data):
                    login_user(user)            
                    return redirect(url_for('user'))
                else:             
                    return redirect(url_for('login'))
        return render_template('admin_signin.html',form=form)
    form=LoginForm()
    return render_template('admin_signin.html',form=form)
# # registration
@app.route('/nautilus-admin/sign-up',methods=['GET','POST'])
def register(): 
    form=RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            email=form.email.data
            if email and hashed_password:
                admin_user=AdminUser(email=email,password1=hashed_password)
                db.session.add(admin_user)
                db.session.commit()
                return redirect(url_for('user'))
        if request.method == 'GET':            
            return render_template('admin_signup.html',form=form)
    return render_template('admin_signup.html',form=form)

@app.route('/logout')
def logout():   
    logout_user()
    return redirect(url_for('user'))




# user
@app.route('/report/form',methods=['GET','POST'])
def user():
    if request.method == 'POST':
        first_name=request.form.get('First-Name',None)
        last_name=request.form.get('Last-Name',None)
        company_email=request.form.get('Company-Email',None)
        company_name=request.form.get('Company-Name',None)
        company_region=request.form.get('Company-Region',None)
        checkbox=request.form.get('checkbox',None)
        user=ConfirmUser(first_name=first_name,last_name=last_name,company_email=company_email,company_name=company_name,company_region=company_region)
        search=ConfirmUser.query.filter_by(company_email=company_email).first()

       
        if search :
            session['user']=company_email 
            return redirect(url_for('question1'))
            # good user
        if not search:
            if checkbox == 'on' :
                db.session.add(user)
                db.session.commit()
                # confirm_email(user)
                session['user']=company_email 
                return redirect(url_for('question1'))

            elif checkbox == 'off':
                db.session.add(user)
                db.session.commit()
                session['user']=company_email 
                return redirect(url_for('question1'))
        naut_email(user)                
    return render_template('form.html')


# email track
def naut_email(user):
    email=user.company_email
    name=user.company_name
    msg = Message('Nautilus Notification',
    sender='noreply@nautilustechnologies.tech',
    recipients=['socials@nautilus.tech','cloudhelpprovider@gmail.com','adedamolabasit09@gmail.com'])
    msg.body=f'''This user just signed up to know what Cloud provider is best for their organization.:
    Company mail = {email}
    company name = {name} '''
    mail.send(msg)
@app.route('/features')
def question1():
    query=Tree.query.all()
    return render_template('branch.html',query=query)
@app.route('/features/<int:question1_id>/')
def question2(question1_id):
    query=db.session.query(Tree).join(Branch1).filter_by(tree_id=question1_id).all()
    return render_template('branch2.html',query=query)
@app.route('/qs1/<int:question1_id>/branch2')
def question3(question1_id):
    tree=Tree.query.join(Branch1).filter_by(id=question1_id).first()
    query=db.session.query(Branch1).join(Branch2).filter_by(branch1_id=question1_id).all()
    
    return render_template('branch3.html',query=query,id=tree.id)
@app.route('/answer/<int:question2_id>')
def answer(question2_id):
    query=Answer.query.filter_by(branch2_id=question2_id).first()
    if g.user:
        user=session['user']
        expert='Speak.an expert'
        firstname=ConfirmUser.query.filter_by(company_email=user).first()
        msg = Message('Your Cloud Help Provider Test Result',
        sender='noreply@nautilustechnologies.tech',
        recipients=[user])
        msg.body=f'''
Hello {firstname.first_name},
Thank you for taking out time to try to Cloud Help Provider (CHP).
{query.main}
CHP Team                                  
        '''
        mail.send(msg)  
    print(request.path)   
    return render_template('branch4.html',query=query)
@app.route('/expert')
def expert():
    return redirect("https://www.nautilus.tech/")

# Terminate
@app.route('/confirmation')
def confirm():
    return render_template('confirmation.html')


if __name__ == "__main__":
    app.run(debug=True)
