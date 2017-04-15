#!/usr/bin/env python
#coding=utf8

import os
import hashlib
import json
from flask import Flask, request, render_template, redirect,make_response, abort, \
                session , g ,url_for, jsonify, make_response
from datetime import datetime
from model import *
import time
from flask_httpauth import HTTPBasicAuth
from collections import OrderedDict
from utils.book_util import *
from utils.user_util import *
from utils.note_util import *
from utils.task_util import *
from werkzeug import secure_filename
from test_qiniu import *


app = Flask(__name__)
auth = HTTPBasicAuth()

@app.teardown_request
def shutdown_session(exception=None):
    session.close()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)



def get_time():
	return time.strftime("%Y-%m-%d %X", time.localtime())


@app.route('/shanbay/user/get/<string:openId>', methods=['GET'])
def user_get_openId(openId):
    return jsonify(get_user(openId))

@app.route('/shanbay/user/get_all', methods=['GET'])
def user_get_all():
    return jsonify(get_all_user())

@app.route('/shanbay/user/update', methods=['POST'])
def user_update():
    tmp_user = request.form.to_dict()
    return jsonify(update_user(tmp_user))

@app.route('/shanbay/user/create', methods=['POST'])
def user_create():
    tmp_user = request.form.to_dict()
    return jsonify(create_user(tmp_user))

@app.route('/shanbay/user/delete/<string:openId>', methods=['GET'])
def user_delete(openId):
    return jsonify(delete_user(openId))

@app.route('/shanbay/user/recover/<string:openId>', methods=['GET'])
def user_recover(openId):
    return jsonify(recover_user(openId))

@app.route('/shanbay/user/login/<string:openId>', methods=['GET'])
def user_login(openId):
    tmp_user = if_user_exist(openId)
    if tmp_user['status']:
        return jsonify(login_user(openId))
    else:
        return jsonify({'status': False})






if __name__ == '__main__':
    app.run(debug=True, port=HOST_PORT, host='0.0.0.0')
