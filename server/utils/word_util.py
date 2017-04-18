#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *

def get_wid(content):
    tmp = {'status':False, 'data':''}
    try:
        tmp['data'] = session.query(Word).filter(Word.content==content).first().wid
        tmp['status'] = True
        return tmp
    except:
        return tmp

def get_word(content):
    tmp = {'status': False}
    tmp_word = session.query(Word).filter(Word.content==content).first()
    if tmp_word:
        tmp['data'] = tmp_word.get_dict()
        tmp['status'] = True
        return tmp
    else:
        tmp['info'] = 'no such word'
        return tmp

def create_word(wdata):
    tmp = {'status': False}
    tmp_word = session.query(Word).filter(Word.content==wdata['content']).first()
    try:
        if not tmp_word:
            tmp_word = Word()
            tmp_word.init_word(wdata)
            session.add(tmp_word)
        else:
            tmp_word.init_word(wdata)
        session.commit()
        tmp['status'] = True
        return tmp
    except Exception, e:
        print Exception, e
        return tmp

def delete_word(content):
    tmp = {'status': False}
    tmp_word = session.query(Word).filter(Word.content==wdata['content']).first()
    try:
        if tmp_word:
            session.delete(tmp_word)
            session.commit()
            tmp['status'] = True
            return tmp
        else:
            tmp['info'] = 'no such word'
            return tmp
    except Exception, e:
        print Exception, e
        return tmp
