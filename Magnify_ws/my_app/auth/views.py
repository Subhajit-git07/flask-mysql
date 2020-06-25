import ldap
from flask import request, render_template, flash, redirect, \
    url_for, Blueprint, g
#from flask.ext.login import 
from flask_login import current_user, login_user, \
    logout_user, login_required
from my_app import login_manager, db, mysql
from my_app import cache
from my_app.auth.models import User, LoginForm

from flask_cors import CORS, cross_origin

import requests
import math

from flask import Flask, abort, json, request, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth

 
auth = Blueprint('auth', __name__)
CORS(auth)
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
 
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
 
 
@auth.before_request
def get_current_user():
    g.user = current_user
 
 
@auth.route('/')
@auth.route('/login', methods=['GET','POST'])
@cache.cached(timeout=50)
def login():
    if current_user.is_authenticated:
        return 'You are already logged in.'

    if request.json:
        username = (request.json.get('username')).upper()
        password = request.json.get('password')
 
        try:
            User.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:
            #return "failure"
            return jsonify({"result":"failure"})

        user = User.query.filter_by(username=username).first()
 
        if not user:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        #return "Success"
        return jsonify({"result":"success"})

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
