from . import _api
from flask import flash, render_template, Flask, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
from app import app
from datetime import datetime
import uuid
from passlib.hash import pbkdf2_sha256

global mongo
mongo = PyMongo(app)
api_version = 1.0   

@_api.before_request
def api_version_function():
    global api_version
#root dir#
@_api.route('/', methods=['GET'])
def api_home():
        return render_template('api.html')
#customer dir#
@_api.route('/ui/user/new/customer', methods=['GET', 'POST'])
def api_customer():
    if request.method == 'GET':
        return render_template('Signup.html')
    
    if request.method == 'POST':
        user_data = {
            '_id': uuid.uuid4().hex,
            'Username': request.form.get('Username'),
            'Email': request.form.get('Email'),
            'Password': request.form.get('Password'),
            'created': datetime.now()
        }
        user_data['Password'] = pbkdf2_sha256.encrypt(user_data['Password'])
        print(user_data)
        if mongo.db.customer.find_one({"Username": user_data['Username']}) or mongo.db.customer.find_one({"Email": user_data['Email']}):   
            return redirect(url_for("public.login"))
        else:
            mongo.db.customer.insert_one(user_data)
            print('Username:', user_data['Username'])
            print('Password:', user_data['Password'])
            print('Email:', user_data['Email'])
            return render_template('ui.html', title='Business Login')
       

    return "Invalid request method."      
#business dir#
@_api.route('/ui/user/new/business', methods=['GET', 'POST'])
def api_business():
    if request.method == 'GET':
        return render_template('Signup.html')

    if request.method == 'POST':
        user_data = {
            '_id': uuid.uuid4().hex,
            'Username': request.form.get('Username'),
            'Email': request.form.get('Email'),
            'Password': request.form.get('Password'),
            'created': datetime.now()
        }
        user_data['Password'] = pbkdf2_sha256.encrypt(user_data['Password'])

        try:
            mongo.db.business.find_one({"Username": user_data['Username']})
            mongo.db.business.find_one({"Email": user_data['Email']})
            mongo.db.business.find_one({"Password": user_data['Password']})
            return render_template("Signup.html")
        
        except:
            mongo.db.business.insert_one(user_data)
            print('Username:', user_data['Username'])
            print('Password:', user_data['Password'])
            print('Email:', user_data['Email'])
            return render_template('ui.html', title='Business Login')

    return "Invalid request method."      

#user dir#
@_api.route('/ui/user/user/new', methods=['GET', 'POST'])
def api_user():
    if request.method == 'GET':
        return render_template('Signup.html')

    if request.method == 'POST':
        user_data = {
            '_id': uuid.uuid4().hex,
            'Username': request.form.get('Username'),
            'Email': request.form.get('Email'),
            'Password': request.form.get('Password'),
            'created': datetime.now()
        }
        user_data['Password'] = pbkdf2_sha256.encrypt(user_data['Password'])
        
        try:
            mongo.db.user.find_one({"Username": user_data['Username']})
            mongo.db.user.find_one({"Email": user_data['Email']})
            mongo.db.user.find_one({"Password": user_data['Password']})
            return render_template("Signup.html")
        
        except:
            mongo.db.users.insert_one(user_data)
            print('Username:', user_data['Username'])
            print('Password:', user_data['Password'])
            print('Email:', user_data['Email'])
            return render_template('ui.html', title='Business Login')
            

           ## if mongo.db.users.find_one({'Email': user_data['Email']}):
             ##   return jsonify({"error":"Email address already in use"}), 400
        
            return render_template('ui.html', title='Business Login')
        else:
            return "Failed to insert user data into the database."
    
######################################################################################
#####################################UI###############################################
######################################################################################
#root for ui dir#
@_api.route('/ui')
def api_ui():
    return render_template('ui.html')
#business dir#
@_api.route('/ui/business', methods=['Get'])
def api_uibusiness():
    business = mongo.db.business.find({
    })
    business_list = []
    for user in business:
        business_list.append(user)
    return render_template('business.html', title='business', businesses=business_list)

#customer dir#
@_api.route('/ui/customer', methods=['Get'])
def api_uicustomer():
    customers = mongo.db.customer.find({
    })
    customer_list = []
    for user in customers:
        customer_list.append(user)
    return render_template('customer.html', title='customers', customers=customer_list)

#user dir#
@_api.route('/ui/user', methods=['Get'])
def api_uiuser():
    users = mongo.db.users.find({
    })
    users_list = []
    for user in users:
        users_list.append(user)
    return render_template('user.html', title='users', users=users_list)
#extra dir#
@_api.route('/ui/user/new', methods=['Get'])
def api_add_user():
    return render_template('add_user.html')
#login dir#
@_api.route('/ui/login', methods=['Get'])
def api_login():
    return render_template('Login.html')
