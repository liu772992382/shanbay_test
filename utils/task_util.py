#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *

def get_tasks_user(openId):
    tmp = {'status': False, 'data':[]}
    tmp_uid = get_uid(openId)
    if tmp_uid['status']:
        try:
            tmp_tasks = session.query(Task).filter(Task.uid==tmp_uid['data'] and Task.status==1).all()
            for i in tmp_tasks:
                tmp_task = i.get_dict()
                tmp_task['word'] = session.query(Word).filter(Word.wid==i.wid).first().get_dict()
                tmp['data'].append(tmp_task)
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'no such user'
        return tmp

def create_tasks(openId):
    tmp = {'status': False}
    tmp_user = session.query(User).filter(User.openId==openId).first()
    if tmp_user:
        try:
            tmp_words = session.query(WordBook).filter(WordBook.bid==tmp_user.enLevel).all()
            for i in tmp_words:
                tmp_task = Task(uid=tmp_user.uid, wid=tmp_user.enLevel)
                session.add(tmp_task)
            session.commit()
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp

def set_daily_tasks(openId):
    tmp = {'status': False}
    tmp_user = session.query(User).filter(User.openId==openId).first()
    if tmp_user:
        tmp_book = session.query(Book).filter(Book.bid==tmp_user.enLevel).first()
        tmp_tasks = session.query(Task).filter(Task.uid==tmp_user.uid and Task.status==0).order_by(func.random()).limit(tmp_user.task).all()
        try:
            for i in tmp_tasks:
                i.status = 1
            session.commit()
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'no such user'
        return tmp




def tag_task(openId, content, tag):
    tmp = {'status': False}
    tmp_uid = get_uid(openId)
    tmp_wid = get_wid(content)
    if tmp_uid['status'] and tmp_wid['status']:
        try:
            tmp_task = session.query(Task).filter(Task.uid==uid and Task.wid==wid).first()
            if tmp_task:
                tmp_task.status = tag
                session.commit()
                tmp['status'] = True
                return tmp
            else:
                tmp['info'] = 'no such task'
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'no such user or word'
        return tmp

def tag_date_task(openId):
    tmp = {'status': False}
    tmp_uid = get_uid(openId)
    tmp_time = datetime.today()
    if tmp_uid['status']:
        try:
            tmp_tasks = session.query(Task).filter(and_(Task.uid==tmp_uid['data'], extract('year', Task.date)==tmp_time.year,extract('month', Task.date)==tmp_time.month,extract('day', Task.date)==tmp_time.day,Task.status==1)).all()
            for i in tmp_tasks:
                i.status = 2
            session.commit()
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'no such user'
        return tmp


def delete_task(openId, content):
    tmp = {'status': False}
    tmp_uid = get_uid(openId)
    tmp_wid = get_wid(content)
    if tmp_uid['status'] and tmp_wid['status']:
        tmp_task = session.query(Task).filter(Task.uid==tmp_uid['data'] and Task.wid==tmp_wid['data']).first()
        if tmp_task:
            try:
                session.delete(tmp_task)
                session.commit()
                tmp['status'] = True
                return tmp
            except Exception, e:
                print Exception, e
                return tmp
        else:
            tmp['info'] = 'no such task'
            return tmp
    else:
        tmp['info'] = 'no such user or word'
        return tmp
