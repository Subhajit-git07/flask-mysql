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


 
Error_dictionary = Blueprint('Error_dictionary', __name__)
     

@Error_dictionary.route('/error_dictionary',methods=['GET','POST'])
@cache.cached(timeout=50)
def index7():
    cur = mysql.connection.cursor()
    query1 = "select id,vocab from dictionary where active = 'Y';"
    #param = (status,id)
    cur.execute(query1)
    data = cur.fetchall()
    data_list = []
    for i in data:
        data_dict = {}
        data_dict["id"] = i[0]
        data_dict["vocab"] = i[1]
        data_list.append(data_dict)
    return jsonify(data_list)
