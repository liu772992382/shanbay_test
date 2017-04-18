#!/usr/bin/env python
#coding=utf8

from config import *


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
