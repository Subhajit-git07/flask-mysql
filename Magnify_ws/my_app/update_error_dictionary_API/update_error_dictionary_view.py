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


 
Update_error_dictionary = Blueprint('Update_error_dictionary', __name__)
     

@Update_error_dictionary.route('/update_error_dictionary',methods=['GET','POST','PUT'])
@cache.cached(timeout=50)
def index8():
    cur = mysql.connection.cursor()
    if request.json:
        id = request.json.get('id')
        active = request.json.get('active')
    query1 = "update dictionary set active=%s where id=%s;"
    param = (active,id)
    try:
        cur.execute(query1,param)
        mysql.connection.commit()
        return jsonify({"result":"success"})
    except Exception as e:
        print(e)
        return jsonify({"result":"failure"})

