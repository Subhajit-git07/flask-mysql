
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

 
report = Blueprint('report', __name__)

@report.route('/Report_API', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def index6():
    cur = mysql.connection.cursor()
    if request.json:
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')
        try:
            page_no = int(request.json.get('page_no'))
        except Exception as e:
            page_no = 0
    if page_no == -1:
        query = "select count(*), log_str, time from new_anomalies where time between %s and %s  group by log_str, time;"
        param = (start_date + ' 00:00:00', end_date + ' 23:59:59')
        cur.execute(query,param)
        data = cur.fetchall()
        return jsonify(data)

    query = "select count(*), log_str, time from new_anomalies where time between %s and %s  group by log_str, time LIMIT 25 OFFSET %s;"
    param = (start_date + ' 00:00:00', end_date + ' 23:59:59', page_no)
    cur.execute(query,param)
    data = cur.fetchall()
    return jsonify(data)

