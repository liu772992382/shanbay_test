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
from utils.moment_util import *
from utils.user_util import *
from utils.activity_util import *
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




if __name__ == '__main__':
    app.run(debug=True, port=HOST_PORT, host='0.0.0.0')
