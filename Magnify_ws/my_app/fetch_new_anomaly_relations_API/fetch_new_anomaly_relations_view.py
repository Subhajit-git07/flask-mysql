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

 
Fetch_new_anomaly_relations = Blueprint('Fetch_new_anomaly_relations', __name__)


@Fetch_new_anomaly_relations.route('/fetch_new_anomaly_relations',methods=['GET','POST'])
@cache.cached(timeout=50)
def index4():
    cur = mysql.connection.cursor()
    if request.json:
        id = request.json.get('id')
        try:
            page_no = int(request.json.get('page_no'))
        except Exception as e:
            page_no = 0

    
    query1 = "select rel_log_str, count, similarity  from ariba_logs.new_anomaly_relations where id=%s;"
    param = (id,)
    cur.execute(query1,param)
    data = cur.fetchall()
    new_array = []

    for i in data:
        rel_log_dict = {}
        rel_log_dict["rel_log_str"] = i[0];
        rel_log_dict["count"] = i[1];
        rel_log_dict["similarity"] = i[2];
        new_array.append(rel_log_dict);
        #new_array.append("".join(i))
    return jsonify(new_array)
