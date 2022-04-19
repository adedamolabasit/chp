from itertools import product
from locale import currency
from nturl2path import url2pathname
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
from flask_mail import Mail

admin=Admin(app,template_mode='bootstrap3',name='Nautilus Admin')
mail=Mail(app)
class Controllers(ModelView):
    pass

admin.add_view(Controllers(Parent,db.session,name='Fisrt Question'))
admin.add_view(Controllers(Heading,db.session,name='Heading'))
admin.add_view(Controllers(Child1,db.session,name='child'))
admin.add_view(Controllers(Tree,db.session,name='First Question'))
admin.add_view(Controllers(Branch1,db.session,name='Second Question'))
admin.add_view(Controllers(Branch2,db.session,name='Third Question'))
admin.add_view(Controllers(Answer,db.session,name='Summary and Email body'))
admin.add_view(Controllers(ConfirmUser,db.session,name='Email Collections'))
admin.add_view(Controllers(AdminUser,db.session,name='Nautilus Admin'))
@app.before_request
def before_request():
    g.user = None
    g.mail=None
    if 'urls' in session:
        g.user = session['urls']
    elif 'mail' in session:
        g.mail = session['mail']
@app.route('/')
def index():
    session['urls']=request.path
    return render_template('chp_1.html')
@app.route('/prompt')
def prompt():
    session['urls']=request.path
    return render_template('chp_2.html')
@app.route('/chp1')
def parent():
    session['urls']=request.path
    # 8545 in css naut
    query=Parent.query.order_by(Parent.id).all()
    return render_template('chp_3.html',query=query)
@app.route('/options',methods=["POST","GET"])
def child1():
    session['urls']=request.path
    options=request.form.getlist('check',None)
    print(options)
    if len(options) == 1:
        return redirect(url_for('question2',id=options))
    if len(options) == 0:
        return redirect(url_for('prompt'))
    headings=Heading.query.join(Heading.parent).filter(Parent.id.in_(options)).first()
    return render_template('chp_4.html',headings=headings)

@app.route('/report/<int:id>')
def report(id):
    session['urls']=request.path
    query=Child1.query.filter_by(id=id).first()
    if query is None:
        abort(404)
   
    mail_session=session.get('mail',None)
    if mail_session:
        active=True
        query=Child1.query.filter_by(id=id).first()
        msg = Message('Your Cloud Help Provider Test Result',
        sender='noreply@nautilustechnologies.tech',
        recipients=[mail_session])
        msg.body=f'''
Hello,
{query.mail_response}
Thank you for taking out time to try to Cloud Help Provider (CHP).
            
                                                CHP Team  
             '''
        mail.send(msg)
    else:
        active=False

    
    return render_template('summary-page.html',query=query,active=active)


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
    path=session['urls'].rsplit('/',1)[-1]
    illegal_path= session['urls'].rsplit('/',1)[-2]
    if illegal_path != '/report':
        return redirect(url_for('prompt'))
    elif illegal_path != '/answer':
        return redirect(url_for('prompt'))
    if request.method == 'POST':
        first_name=request.form.get('First-Name',None)
        last_name=request.form.get('Last-Name',None)
        company_email=request.form.get('Company-Email',None)
        company_name=request.form.get('Company-Name',None)
        company_region=request.form.get('Company-Region',None)
        user=ConfirmUser(first_name=first_name,last_name=last_name,company_email=company_email,company_name=company_name,company_region=company_region)
        search=ConfirmUser.query.filter_by(company_email=company_email).first()    
        if search :
            if illegal_path == '/report':
                query=Child1.query.filter_by(id=path).first()
            if illegal_path == '/answer':
                query=Child1.query.filter_by(id=path).first()
            email=user.company_email
            msg = Message('Your Cloud Help Provider Test Result',
            sender='noreply@nautilustechnologies.tech',
            recipients=[email])
            msg.body=f'''
Hello,
{query.mail_response}

Thank you for taking out time to try to Cloud Help Provider (CHP).
            
                                                CHP Team  
             '''
            mail.send(msg)
           

            flash('Thank you! Your submission has been recieved','success')
            session['mail']=user.company_email
            a=session.get('mail')
            print(a)
            return redirect(url_for('prompt'))
        if not search:
            db.session.add(user)
            db.session.commit()
            path=session['urls'].rsplit('/','1')[-1]
            query=Child1.query.filter_by(id=path).first()
            email=user.company_email
            msg = Message('Your Cloud Help Provider Test Result',
            sender='noreply@nautilustechnologies.tech',
            recipients=[email])
            msg.body=f'''
Hello,
{query.mail_response}
Thank you for taking out time to try to Cloud Help Provider (CHP).
            
                                                CHP Team  
             '''
            mail.send(msg)
            return redirect(url_for('prompt'))  
       
    return render_template('email-collection.html')


# email track
def naut_email(user,path):
    session['urls']=request.path
    
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
    session['urls']=request.path
    query=Tree.query.all()
    return render_template('chp_5.html',query=query)
@app.route('/features/<int:id>/')
def question2(id):
    session['urls']=request.path
    query=db.session.query(Tree).join(Branch1).filter_by(tree_id=id).all()
    return render_template('chp_6.html',query=query)
@app.route('/qs1/<int:question1_id>/branch2')
def question3(question1_id):
    session['urls']=request.path
    tree=Tree.query.join(Branch1).filter_by(id=question1_id).first()
    back=tree.id
    query=db.session.query(Branch1).join(Branch2).filter_by(branch1_id=question1_id).all()
    
    return render_template('chp_7.html',query=query,id=tree.id,back=back)
@app.route('/answer/<int:question2_id>')
def answer(question2_id):
    session['urls']=request.path
    query=Answer.query.filter_by(branch2_id=question2_id).first()
    back=query.id
    mail_session=session.get('mail',None)
    if mail_session:
        active=True
        query=Child1.query.filter_by(id=question2_id).first()
        msg = Message('Your Cloud Help Provider Test Result',
        sender='noreply@nautilustechnologies.tech',
        recipients=[mail_session])
        msg.body=f'''
Hello,
{query.mail_response}
Thank you for taking out time to try to Cloud Help Provider (CHP).
            
                                                CHP Team  
             '''
        mail.send(msg)
    else:
        active=False
    return render_template('summary-page2.html',query=query,back=back,active=active)

# Terminate
@app.route('/confirmation',methods=['POST','GET'])
def confirm():
    if request.method == 'POST':
        confirm=request.form.get('confirm')
        if confirm:
            session.close()
    previous_url=session.get('urls','/')

    return render_template('confirm.html',previous_url=previous_url)


if __name__ == "__main__":
    app.run(debug=True)
