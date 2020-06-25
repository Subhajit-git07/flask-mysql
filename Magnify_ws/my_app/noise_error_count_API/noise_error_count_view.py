from flask import request, render_template, flash, redirect, \
    url_for, Blueprint, g
from flask_login import current_user, login_user, \
    logout_user, login_required
from my_app import db, mysql
from my_app import cache

import requests
import math
import pandas as pd

from flask import Flask, abort, json, request, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth

from datetime import datetime

 
Noise_error_count = Blueprint('Noise_error_count', __name__)

@Noise_error_count.route('/noise_error_count', methods=['GET', 'POST'])
@cache.cached(timeout=50)
def index11():
    cur = mysql.connection.cursor()
    if request.json:
        start_time = request.json.get('start_time')
        end_time = request.json.get('end_time')
        try:
            page_no = int(request.json.get('page_no'))
        except Exception as e:
            page_no = 0
    
    date_format = "%Y-%m-%d"
    a = datetime.strptime(start_time, date_format)
    b = datetime.strptime(end_time, date_format)
    delta = b - a
    periods = (delta.days + 1) * 24
    #print(delta.days)
    start = start_time
    end = end_time
    rng = pd.date_range(start, freq='H', periods=periods)
    empty_df = pd.DataFrame({ 'time': rng, "noise_count":0, "error_count":0 }) 
    empty_df['time'] = pd.to_datetime(empty_df['time'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%d-%m-%y %H:%M:%S')
        
    #query = "select sum(count), DATE_FORMAT(time,'%%d/%%m/%%Y %%h:%%m:%%s') as time  from logged_noise_summary where time between %s and %s group by DATE_FORMAT(time,'%%d/%%m/%%Y %%h:%%m:%%s');"
    #query = "select sum(count), DATE_FORMAT(MIN(time),'%%d-%%m-%%Y %%H:%%i:00') AS tmstamp  from logged_noise_summary where time between %s and %s  group by UNIX_TIMESTAMP(time) div 300;"
    query1 = "select sum(count),date_format(time, '%%d-%%m-%%y %%h:00:00') as time from logged_noise_summary where time between %s and %s group by date_format(time, '%%d-%%m-%%y %%h:00:00');"
    query2 = "select sum(count),date_format(time, '%%d-%%m-%%y %%h:00:00') as time from logged_errors_summary where time between %s and %s group by date_format(time, '%%d-%%m-%%y %%h:00:00');"

    param = (start_time + ' 00:00:00', end_time + ' 23:59:59')
    cur.execute(query1,param)
    noise_data = cur.fetchall()

    cur.execute(query2,param)
    error_data = cur.fetchall()

    #return jsonify(len(error_data))


    noise_count_list = []
    for i in noise_data:
        noise_count_dict = {}
        noise_count_dict["noise_count"] = str(i[0])
        noise_count_dict["time"] = str(i[1])
        noise_count_list.append(noise_count_dict)
    #return jsonify(noise_count_list)

    error_count_list = []
    for j in error_data:
        error_count_dict = {}
        error_count_dict["error_count"] = str(j[0])
        error_count_dict["time"] = str(j[1])
        error_count_list.append(error_count_dict)
    #return jsonify(error_count_list)

    noise_error_list = []
   

    if len(noise_data) == 0 and len(error_data) != 0:
        for k in error_count_list:
            k.update({"noise_count":"0"})
            noise_error_list.append(k)
        #return jsonify(noise_error_list)
        noise_error_df = pd.DataFrame(noise_error_list)
        df_merge = pd.concat([empty_df,noise_error_df],sort=True).drop_duplicates('time',keep='last').sort_values(by=['time']).reset_index(drop=True)
        return jsonify(df_merge.to_dict('records'))

    if len(error_data) == 0 and len(noise_data) != 0:
        for m in noise_count_list:
            m.update({"error_count":"0"})
            noise_error_list.append(m)
        #return jsonify(noise_error_list)
        noise_error_df = pd.DataFrame(noise_error_list)
        df_merge = pd.concat([empty_df,noise_error_df],sort=True).drop_duplicates('time',keep='last').sort_values(by=['time']).reset_index(drop=True)
        return jsonify(df_merge.to_dict('records'))



    if len(noise_data) != 0 and len(error_data) != 0:
        noise_df = pd.DataFrame(noise_count_list)
        error_df = pd.DataFrame(error_count_list)
        final_df = pd.merge(noise_df, error_df, on="time",how='outer').fillna(0)
        #final_dict = final_df.to_dict('records')
        #return jsonify(final_dict)
        df_merge = pd.concat([empty_df,final_df],sort=True).drop_duplicates('time',keep='last').sort_values(by=['time']).reset_index(drop=True)
        return jsonify(df_merge.to_dict('records'))

    if len(noise_data) == 0 and len(error_data) == 0:
        #return jsonify("No noise or error data present")
        return jsonify(empty_df.to_dict('records'))
        
        


    


