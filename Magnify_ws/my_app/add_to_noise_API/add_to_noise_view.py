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


 
Add_to_noise = Blueprint('Add_to_noise', __name__)
     

@Add_to_noise.route('/add_to_noise',methods=['GET','POST','PUT'])
@cache.cached(timeout=50)
def index12():
    cur = mysql.connection.cursor()
    updateCur = mysql.connection.cursor()
    #if request.json:
        #id = request.json.get('id')
        #stacktrace = request.json.get('stacktrace')
    stacktrace = request.args.get('stacktrace')
    
    query1 = "select id,status from new_anomalies where log_str =%s;"
    query2 = "insert into new_anomalies(log_str, count, status) values(%s, 1, 'N');"
    query3 = "update new_anomalies set status = 'N' where id = %s;"

    param = (stacktrace,)
    try:
        count = cur.execute(query1,param)
        data = cur.fetchall()
        if count == 0:
            cur.execute(query2,param)
            mysql.connection.commit()
            return jsonify({"result":"success"})
        else :
            for i in data:
                log_id = i[0]
                status = i[1]
                if status != 'N':
                    updateParam = (log_id,)
                    updateCur.execute(query3,updateParam)
                    mysql.connection.commit()
                    
                    return jsonify({"result":"success"})
                else:
                    return jsonify({"result":"failure. Record already exists in noise database with record id : "+str(log_id)})
            
                break

    except Exception as e:
        print(e)
        updateCur.close()
        cur.close()
        return jsonify({"result":"failure "+e})

