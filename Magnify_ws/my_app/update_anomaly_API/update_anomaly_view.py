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


 
Update_anomaly = Blueprint('Update_anomaly', __name__)
     

@Update_anomaly.route('/update_anomaly',methods=['GET','POST','PUT'])
@cache.cached(timeout=50)
def index3():
    cur = mysql.connection.cursor()
    if request.json:
        id = request.json.get('id')
        status = request.json.get('type')
    query1 = "update new_anomalies set status=%s where id=%s;"
    param = (status,id)
    try:
        cur.execute(query1,param)
        mysql.connection.commit()
        return jsonify({"result":"success"})
    except Exception as e:
        print(e)
        return jsonify({"result":"failure"})

