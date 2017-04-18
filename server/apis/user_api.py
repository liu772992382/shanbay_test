#!/usr/bin/env python
#coding=utf8

from config import *

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
