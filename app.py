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

admin.add_view(Controllers(Parent,db.session,name='ALL Double Collections'))
admin.add_view(Controllers(Heading,db.session,name='Double Collections Headings'))
admin.add_view(Controllers(Child1,db.session,name='Double Collections'))
admin.add_view(Controllers(Tree,db.session,name='All Single Collections'))
admin.add_view(Controllers(Branch1,db.session,name='Single collections'))
admin.add_view(Controllers(Branch2,db.session,name='Sub Single Collection'))
admin.add_view(Controllers(Answer,db.session,name='Single Collection Summary and Mail Summary'))
admin.add_view(Controllers(ConfirmUser,db.session,name='User Email Collections'))
admin.add_view(Controllers(AdminUser,db.session,name='Nautilus Administrator'))
@app.before_request
def before_request():
    g.user = None
    g.mail=None
    if 'urls' in session:
        g.user = session['urls']
    elif 'mail' in session:
        g.mail = session['mail']

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('parent'))
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('parent'))
    
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
   
    queries=Parent.query.order_by(Parent.id).all()


    return render_template('chp_3.html',query=queries)
@app.route('/options',methods=["POST","GET"])
def child1():
    session['urls']=request.path
    options=request.form.getlist('check',None)
    print(options)
    if len(options) == 1:
        flash('select two responses','danger')
        abort(404)
    if len(options) == 0:
        flash('select two responses','danger')
        abort(404)
    if len(options) > 3:
        flash('select two responses','danger')
        abort(404)
    headings=Heading.query.join(Heading.parent).filter(Parent.id.in_(options)).first()
    return render_template('chp_4.html',headings=headings)

@app.route('/report/<int:id>')
def report(id):
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
    session['urls']=request.path
    return render_template('summary-page.html',query=query,active=active)


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

@app.route('/form1/<int:id>',methods=['GET','POST'])
def form1(id):
    if request.method == 'POST':
        paths=session.get('urls','/')
        path=paths.rsplit('/',1)[-1]
        first_name=request.form.get('First-Name',None)
        last_name=request.form.get('Last-Name',None)
        company_email=request.form.get('Company-Email',None)
        company_name=request.form.get('Company-Name',None)
        company_region=request.form.get('Company-Region',None)
        user=ConfirmUser(first_name=first_name,last_name=last_name,company_email=company_email,company_name=company_name,company_region=company_region)
        search=ConfirmUser.query.filter_by(company_email=company_email).first()
        if user != None:
            db.session.add(user)
            db.session.commit()
            query=Answer.query.join(Branch2).filter_by(id=id).first()
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
            email=user.company_email
            session['mail']=user.company_email
            return redirect(url_for('message',message=email))
    return render_template('form1.html')
@app.route('/form2/<int:id>',methods=['GET','POST'])
def form2(id):
    if request.method == 'POST':
        paths=session.get('urls','/')
        path=paths.rsplit('/',1)[-1]
        first_name=request.form.get('First-Name',None)
        last_name=request.form.get('Last-Name',None)
        company_email=request.form.get('Company-Email',None)
        company_name=request.form.get('Company-Name',None)
        company_region=request.form.get('Company-Region',None)
        user=ConfirmUser(first_name=first_name,last_name=last_name,company_email=company_email,company_name=company_name,company_region=company_region)
        search=ConfirmUser.query.filter_by(company_email=company_email).first()
        if user != None:
            db.session.add(user)
            db.session.commit()
            query=Child1.query.filter_by(id=id).first()
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
            email=user.company_email
            session['mail']=user.company_email
            return redirect(url_for('message',message=email))
    return render_template('form2.html')
# @app.route('/form/<int:id>',methods=['GET','POST'])
# def form2(id):
#     if request.method == 'POST':
#         first_name=request.form.get('First-Name',None)
#         last_name=request.form.get('Last-Name',None)
#         company_email=request.form.get('Company-Email',None)
#         company_name=request.form.get('Company-Name',None)
#         company_region=request.form.get('Company-Region',None)
#         user=ConfirmUser(first_name=first_name,last_name=last_name,company_email=company_email,company_name=company_name,company_region=company_region)
#         search=ConfirmUser.query.filter_by(company_email=company_email).first()
#         if user != None:
#             db.session.add(user)
#             db.session.commit()
#             query=Child1.query.filter_by(id=id).first()
#             email=user.company_email
#             msg = Message('Your Cloud Help Provider Test Result',
#             sender='noreply@nautilustechnologies.tech',
#             recipients=[email])
#             msg.body=f'''
#     Hello,
#     {query.mail_response}

#     Thank you for taking out time to try to Cloud Help Provider (CHP).
                
#                                                     CHP Team  
#                 '''
#             mail.send(msg)
#             session['mail']=user.company_email
#         return render_template('form2.html')

# user
@app.route('/report/form',methods=['GET','POST'])
def user():
    paths=session.get('urls','/')
    path=paths.rsplit('/',1)[-1]
    illegal_path=paths.rsplit('/',1)[-2]
    # print(illegal_path)
    # if illegal_path != '/report':
    #     return redirect(url_for('prompt'))
    # if illegal_path != '/answer':
    #     return redirect(url_for('prompt'))
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
                session['mail']=user.company_email
                return redirect(url_for('message',message=user.company_email)) 
            elif illegal_path == '/answer':
                query=Answer.query.filter_by(branch2_id=path).first()
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
                session['mail']=user.company_email
                return redirect(url_for('message',message=user.company_email)) 
        if not search:
            db.session.add(user)
            db.session.commit()
            path=session['urls'].rsplit('/','1')[-1]
            if illegal_path == '/report':
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
                naut_email(user)
                return redirect(url_for('message',message=user.company_email))  
            elif illegal_path == 'answer':
                query=Answer.query.filter_by(branch2_id=path).first()
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
                naut_email(user)
                return redirect(url_for('message',message=user.company_email))  
       
    return render_template('email-collection.html',path=path)

@app.route('/message/<string:message>')
def message(message):
    company_email=message
    
    return render_template('message.html',query=company_email)
# email track
def naut_email(user):
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
    illegal_path= session['urls'].rsplit('/',1)[-2]
    print(illegal_path)
    query=Answer.query.filter_by(branch2_id=question2_id).first()
    back=query.id
    mail_session=session.get('mail',None)
    if mail_session:
        active=True
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
    previous_url=session.get('urls')
    

    return render_template('confirm.html',previous_url=previous_url)




if __name__ == "__main__":
    app.run(debug=True)
