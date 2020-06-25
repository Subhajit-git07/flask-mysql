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


 
Noise_count = Blueprint('Noise_count', __name__)

@Noise_count.route('/noise_count', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def index10():
    cur = mysql.connection.cursor()
    if request.json:
        start_time = request.json.get('start_time')
        end_time = request.json.get('end_time')
        try:
            page_no = int(request.json.get('page_no'))
        except Exception as e:
            page_no = 0
            
    query = "select sum(count), DATE_FORMAT(MIN(time),'%%d-%%m-%%Y %%H:%%i:00') AS tmstamp  from logged_noise_summary where time between %s and %s  group by UNIX_TIMESTAMP(time) div 300;"
    #param = (start_time + ' 00:00:00', end_time + ' 23:59:59', page_no)
    param = (start_time + ' 00:00:00', end_time + ' 23:59:59')
    cur.execute(query,param)
    data = cur.fetchall()
    cur.close()
    noise_count_list = []
    for i in data:
        #print(i[0])
        #print(i[1])
        noise_count_dict = {}
        noise_count_dict["count"] = str(i[0])
        noise_count_dict["time"] = str(i[1])
        noise_count_list.append(noise_count_dict)

    #print (noise_count_list)
    return jsonify(noise_count_list)


