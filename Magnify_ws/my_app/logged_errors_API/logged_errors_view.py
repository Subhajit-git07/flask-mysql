from flask import request, render_template, flash, redirect, \
    url_for, Blueprint, g
from flask_login import current_user, login_user, \
    logout_user, login_required
from my_app import db, mysql
from my_app import cache

import requests
import math

from flask import Flask, abort, json, request, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth

 
Logged_errors = Blueprint('Logged_errors', __name__)
     

@Logged_errors.route('/specific_logged_errors',methods=['GET','POST'])
@cache.cached(timeout=50)
def index9():
    cur = mysql.connection.cursor()
    if request.json:
        start_time = request.json.get('start_time')
        end_time = request.json.get('end_time')
        ids      = request.json.get('ids')
    ids = json.loads(ids)
    
    data_list = []
    for i in ids:
        query1 = "select date_format(time, '%%y-%%m-%%d %%h:%%m:%%s'), log_str from logged_errors where id=%s and time between %s and %s;"
        param = (i,start_time, end_time)
        cur.execute(query1,param)
        data = cur.fetchall()
        for j in data:
            data_dict = {}
            data_dict["time"] = j[0]
            data_dict["log"]  = j[1]
            data_list.append(data_dict)
    return jsonify(data_list)
