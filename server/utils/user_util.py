#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *
from werkzeug.security import generate_password_hash, check_password_hash
import copy



def get_uid(openId):
    tmp = {'status':False, 'data':''}
    try:
        tmp['data'] = session.query(User).filter(User.openId==openId).first().uid
        tmp['status'] = True
        return tmp
    except:
        return tmp

def get_user(openId):
    tmp = {'status':False, 'data':[]}
    tmp_user = session.query(User).filter(User.openId==openId and not User.isDel).first()
    if tmp_user:
        try:
            tmp['data'] = tmp_user.get_dict()
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'No such user'
        return tmp


def get_all_user():
    tmp = {'status':False, 'data':[]}
    try:
        users = session.query(User).filter(not User.isDel).all()
        for i in users:
            tmp['data'].append(i.get_dict())
        tmp['status'] = True
        return tmp
    except Exception, e:
        print Exception, e
        return tmp

def if_user_exist(openId):
    tmp = {'status':False}
    tmp_user = session.query(User).filter(User.openId==openId).all()
    if tmp_user != []:
        tmp['data'] = tmp_user
        tmp['status'] = True
        return tmp
    else:
        return tmp


def create_user(user_data):
    tmp = {'status':False}
    if not if_user_exist(user_data['openId'])['status']:
        tmp_user = User()
        tmp_user.loginTime = datetime.today()
        tmp_user.init_user(user_data)
        try:
            session.add(tmp_user)
            session.commit()
            tmp['data'] = tmp_user.uid
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'this user is existed!'
        return tmp

def recover_user(openId):
    tmp = {'status': False}
    tmp_user = session.query(User).filter(User.openId==openId and User.isDel).first()
    if tmp_user:
        tmp_user.isDel = False
        session.commit()
        tmp['status'] = True
        return tmp
    else:
        tmp['info'] = 'no such user or this user is not deleted'
        return tmp

def update_user(user_data):
    tmp = {'status':False}
    # print kwargs['openId']
    print user_data
    if if_user_exist(user_data['openId'])['status']:
        tmp_user = session.query(User).filter(User.openId==user_data['openId']).first()
        try:
            tmp_user.init_user(user_data)
            session.commit()
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            tmp['info'] = 'error'
            return tmp
    else:
        tmp['info'] = 'no such user'
        return tmp

def delete_user(openId):
    tmp = {'status':False}
    tmp_user = if_user_exist(openId)
    if tmp_user['status']:
        try:
            tmp_user['data'].isDel = True
            session.commit()
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'no such user'
        return tmp


def login_user(openId):
    tmp = {'status':False}
    tmp_user = session.query(User).filter(User.openId==openId).first()
    if tmp_user:
        tmp_user.loginTime = datetime.today()
        tmp['data'] = copy.deepcopy(tmp_user.get_dict())
        session.commit()
        tmp['status'] = True
        return tmp
    else:
        return tmp
