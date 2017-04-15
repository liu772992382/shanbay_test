#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *

def get_tasks_user(uid):
    tmp = {'status': False, 'data':[]}
    try:
        tmp_tasks = session.query(Task).filter(Task.uid==uid).all()
        for i in tmp_tasks:
            tmp_task = i.get_dict()
            tmp_task['word'] = session.query(Word).filter(Word.wid-=i.wid).first().get_dict()
            tmp['data'].append(tmp_task)
        tmp['status'] = True
        return tmp
    except Exception, e:
        print Exception, e
        return tmp

def create_tasks(uid, bid):
    tmp = {'status': False}
    try:
        tmp_words = session.query(WordBook).filter(WordBook.bid==bid).all()
        for i in tmp_words:
            tmp_task = Task(uid=uid, wid=i.wid)
            session.add(tmp_task)
        session.commit()
        tmp['status'] = True
        return tmp
    except Exception, e:
        print Exception, e
        return tmp

def tag_task(uid, wid, tag):
    tmp = {'status': False}
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

def delete_task(uid, wid):
    tmp = {'status': False}
    tmp_task = session.query(Task).filter(Task.uid==uid and Task.wid==wid).first()
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
