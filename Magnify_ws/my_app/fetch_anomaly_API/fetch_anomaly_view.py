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


 
Fetch_anomaly = Blueprint('Fetch_anomaly', __name__)

@Fetch_anomaly.route('/fetch_anomaly', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def index():
    cur = mysql.connection.cursor()
    if request.json:
        start_time = request.json.get('start_time')
        end_time = request.json.get('end_time')
        status = request.json.get('status')
        try:
            page_no = int(request.json.get('page_no'))
        except Exception as e:
            page_no = 0
    #query = "select log_str, count, status, id  from ariba_logs.new_anomalies where time>=%s and time<=%s LIMIT 25 OFFSET %s;"
    page_no = page_no * 500 
    if status:
        #query = "select log_str, count, status, id  from ariba_logs.new_anomalies where time between %s and %s and status=%s order by count desc LIMIT 25 OFFSET %s;"
        query = "select na.log_str, na.count, na.status,  na.id, ifnull(nar_cnt.cnt,0) as ref_count from new_anomalies na left outer join (select nar.id, count(nar.rel_id) as cnt  from  new_anomaly_relations nar group by  nar.id) nar_cnt on  na.id = nar_cnt.id where time between %s and %s and status=%s order by na.id desc LIMIT %s,500;"

        param = (start_time + ' 00:00:00',end_time + ' 23:59:59', status, page_no)
        cur.execute(query,param)
        data = cur.fetchall()
    else:
        query = "select na.log_str, na.count, na.status,  na.id, ifnull(nar_cnt.cnt,0) as ref_count from new_anomalies na left outer join (select nar.id, count(nar.rel_id) as cnt  from  new_anomaly_relations nar group by  nar.id) nar_cnt on  na.id = nar_cnt.id where time between %s and %s order by na.id desc LIMIT %s,500;"
        #query = "select log_str, count, status, id  from ariba_logs.new_anomalies where time between %s and %s order by count desc LIMIT 25 OFFSET %s;"
        param = (start_time + ' 00:00:00',end_time + ' 23:59:59', page_no)
        cur.execute(query,param)
        data = cur.fetchall()

    log_count_list = []
    for i in data:
        log_count_dict_in = {}
        log_count_dict_in["error"] = i[0]
        log_count_dict_in["count"] = i[1]
        log_count_dict_in["type"] = i[2]
        log_count_dict_in["id"] = i[3]
        log_count_dict_in["ref_count"] = i[4]
        log_count_list.append(log_count_dict_in)
    return jsonify(log_count_list)


