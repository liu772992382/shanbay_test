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


#-----------------------用户接口-------------------------------------------
@app.route('/shanbay/user/get/<string:openId>', methods=['GET'])
def user_get_openId(openId):
    return jsonify(get_user(openId))

@app.route('/shanbay/user/get_all', methods=['GET'])
def user_get_all():
    return jsonify(get_all_user())

@app.route('/shanbay/user/update', methods=['POST'])    #更新用户信息
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

@app.route('/shanbay/user/login', methods=['POST']) #用户登陆
def user_login():
    tmp_info = request.form.to_dict()
    if not if_user_exist(tmp_info['openId'])['status']:
        create_user(tmp_info)
    return jsonify(login_user(tmp_info['openId']))


#-----------------------笔记接口-------------------------------------------
@app.route('/shanbay/note/create', methods = ['POST'])  #创建笔记
def note_create():
    tmp_data = request.form.to_dict()
    return jsonify(create_note(tmp_data))

@app.route('/shanbay/note/get_by_word/<string:word>', methods=['GET'])  #根据单词获得笔记
def note_get_by_word(word):
    tmp_notes = get_notes_word(word)
    if tmp_notes['status']:
        for i in tmp_notes:
            i['nickName'] = session.query(User).filter(User.uid==i['uid']).nickName
    return jsonify(tmp_notes)

@app.route('/shanbay/note/get', methods=['GET'])    #获取所有笔记
def note_get():
    return jsonify(get_notes())

@app.route('/shanbay/note/get_by_user/<string:openId>', methods=['GET'])    #根据用户获得笔记
def note_get_by_user(openId):
    tmp_notes = get_notes_user(openId)
    if tmp_notes['status']:
        for i in tmp_notes:
            i['nickName'] = session.query(User).filter(User.uid==i['uid']).nickName
    return jsonify(tmp_notes)

@app.route('/shanbay/note/get_by_user_word/<string:openId>/<string:word>', methods=['GET']) #根据用户和单词获得笔记
def note_get_by_user_word(openId, word):
    tmp_notes = get_notes_user_word(openId, word)
    if tmp_notes['status']:
        for i in tmp_notes:
            i['nickName'] = session.query(User).filter(User.uid==i['uid']).nickName
    return jsonify(tmp_notes)

# @app.route('/shanbay/note/delete/<int:nid>', methods=['GET'])
# def note_delete(nid):
#     return jsonify(delete_note(nid))


#-----------------------单词书接口-------------------------------------------
@app.route('/shanbay/book/create/<string:name>', methods=['GET'])
def book_create(name):
    return jsonify(create_book(name))

@app.route('/shanbay/book/get_all', methods=['GET'])    #获取所有单词书
def book_get_all():
    return jsonify(get_all_books())

@app.route('/shanbay/book/set_wordBook', methods=['POST'])
def wordBook_set(name):
    tmp_words = request.form.get('words')
    tmp_name = request.form.get('name')
    return jsonify(set_wordBook(tmp_words, tmp_name))

@app.route('/shanbay/book/update/<string:name>', methods=['GET'])
def book_update(name):
    return jsonify(name)

# @app.route('/shanbay/book/delete/bid', methods=['GET'])
# def book_delete(bid):
#     return jsonify(delete_book(bid))


#-----------------------单词接口-------------------------------------------
@app.route('/shanbay/word/get/<string:name>', methods=['GET'])
def word_get(content):
    return jsonify(get_word(name))

@app.route('/shanbay/word/create', methods=['POST'])
def word_create():
    tmp_data = request.get('word_data')
    return jsonify(create_word(word_data))

# @app.route('/shanbay/word/delete/<string:content>', methods=['GET'])
# def word_delete(content):
#     return jsonify(delete_word(content))



#-----------------------任务接口-------------------------------------------
@app.route('/shanbay/task/get/<string:openId>', methods=['GET'])    #获取当日任务
def task_get(openId):
    return jsonify(get_tasks_user(openId))

@app.route('/shanbay/task/get_checks/<string:openId>', methods=['GET']) #获取打卡任务
def checks_get(openId):
    return jsonify(get_checks(openId))


@app.route('/shanbay/task/create/<string:openId>', methods=['GET']) #根据单词书创建所有任务
def task_create(openId):
    return jsonify(create_tasks(openId))

@app.route('/shanbay/task/check/<string:openId>', methods=['GET'])  #完成当日打卡
def task_check(openId):
    return jsonify(check_task(openId))

@app.route('/shanbay/task/set_daily/<string:openId>', methods=['GET'])  #设置日常任务
def task_set_daily(openId):
    tmp_uid = get_uid(openId)
    if tmp_uid['status']:
        tmp_check = session.query(Check).filter(and_(Check.uid==tmp_uid['data'], Check.date==datetime.today().date())).first()
        print 'tmp_check', tmp_check
        # tmp_tasks = session.query(Task).filter(and_(Task.uid==get_uid(openId)['']))
        if not tmp_check:
            return jsonify(set_daily_tasks(openId))
        else:
            tmp = {'status': False, 'info': 'daily tasks has set', 'finish': False}
            if tmp_check.status == 0:
                return jsonify(tmp)
            else:
                tmp['finish'] = True
                return jsonify(tmp)
    else:
        return jsonify({'status': False, 'info': 'no such user'})

@app.route('/shanbay/task/tag', methods=['POST'])   #标记完成当前单词
def task_tag():
    tmp_tid = request.form.get('tid')
    tmp_tag = request.form.get('tag')
    print tmp_tag
    return jsonify(tag_task(tmp_tid, tmp_tag))

@app.route('/shanbay/task/tag_date/<string:openId>', methods=['GET'])
def task_tag_date(openId):
    return jsonify(tag_date_task(openId))

# @app.route('/shanbay/task/delete/<string:content>/<string:openId>', methods=['GET'])
# def task_delete(content, openId):
#     return jsonify(delete_task(openId, content))



if __name__ == '__main__':
    app.run(debug=True, port=HOST_PORT, host='0.0.0.0')