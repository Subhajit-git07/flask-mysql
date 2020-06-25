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

 
Fetch_anomaly_count = Blueprint('Fetch_anomaly_count', __name__)
 
@Fetch_anomaly_count.route('/fetch_anomaly_count',methods=['GET','POST'])
@cache.cached(timeout=50)
def index2():
    cur = mysql.connection.cursor()
    if request.json:
        start_time = request.json.get('start_time')
        end_time = request.json.get('end_time')
    query1 = "select count(*) from ariba_logs.new_anomalies where time between %s and %s;"
    param = (start_time + ' 00:00:00', end_time+ ' 23:59:59')
    cur.execute(query1,param)
    total_rows = cur.fetchone()[0]
#    page_count = math.ceil(total_rows/25)
    page_count = total_rows
#    page_number = (str(page_count)+" pages"+","+str(total_rows)+" records")
    count_num_dict = {}
    count_num_dict["total_records"] = page_count
#    count_num_dict["page_number"] = page_number
    return jsonify(count_num_dict)
    

