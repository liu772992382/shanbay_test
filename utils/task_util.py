#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *
from user_util import get_uid
from book_util import get_bid
from word_util import get_wid


# def check_time(tdata):
#     return tdata.date() == datetime.today().date()

def get_tasks_user(openId):
    tmp = {'status': False, 'data':[]}
    tmp_user = session.query(User).filter(User.openId==openId).first()
    if tmp_user:
        try:
            tmp_tasks = session.query(Task).filter(and_(Task.uid==tmp_user.uid, Task.status>=1, Task.date==datetime.today().date())).order_by(Task.tid).limit(tmp_user.task).all()
            cnt = 0
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
            tmp_tasks = session.query(Task).filter(Task.status==0).all()
            for i in tmp_tasks:
                session.delete(i)
            tmp_words = session.query(WordBook).filter(WordBook.bid==tmp_user.enLevel).all()
            for i in tmp_words:
                tmp_task = Task(uid=tmp_user.uid, bid=tmp_user.enLevel, wid=i.wid)
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
        tmp_old_tasks = session.query(Task).filter(and_(Task.uid==tmp_user.uid, Task.status==1)).limit(tmp_user.task).all()
        if len(tmp_old_tasks) < tmp_user.task:
            tmp_tasks = session.query(Task).filter(and_(Task.uid==tmp_user.uid, Task.status==0)).order_by(func.random()).limit(tmp_user.task - len(tmp_old_tasks)).all()
            if tmp_tasks == []:
                tmp['info'] = 'no tasks'
                return tmp
            for i in tmp_tasks:
                i.status = 1
                i.date = datetime.today().date()
        for i in tmp_old_tasks:
            i.date = datetime.today().date()
        tmp_check = Check()
        tmp_check.uid = tmp_user.uid
        session.add(tmp_check)
        session.commit()
        tmp['status'] = True
        return tmp
    else:
        tmp['info'] = 'no such user'
        return tmp




def tag_task(tid, tag):
    tmp = {'status': False}
    try:
        tmp_task = session.query(Task).filter(Task.tid==tid).first()
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

def check_task(openId):
    tmp = {'status': False}
    tmp_uid = get_uid(openId)
    if tmp_uid['status']:
        tmp_check = session.query(Check).filter(and_(Check.uid==tmp_uid['data'], Check.date==datetime.today().date())).first()
        if tmp_check:
            tmp_check.status = 1
            session.commit()
            tmp['status'] = True
            return tmp
        else:
            tmp['info'] = 'no such check'
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

def get_checks(openId):
    tmp = {'status': False, 'data': []}
    tmp_user = session.query(User).filter(User.openId==openId).first()
    if tmp_user:
        tmp_checks = session.query(Check).filter(Check.uid==tmp_user.uid).all()
        cnt = 0
        for i in tmp_checks:
            tmp['data'].append(i.get_dict())
            if i.status == 1:
                cnt += 1
        tmp['amount'] = cnt
        tmp['status'] = True
        return tmp
    else:
        tmp['info'] = 'no such user'
        return tmp
