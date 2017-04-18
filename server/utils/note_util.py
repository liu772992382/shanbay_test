#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *

def create_note(note_data):
    tmp = {'status': False}
    tmp_user = session.query(User).filter(User.openId==note_data['openId']).first()
    if tmp_user:
        tmp_note = Note()
        tmp_note.uid = tmp_user.uid
        tmp_note.init_note(note_data)
        try:
            session.add(tmp_note)
            session.commit()
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'no such user'
        return tmp

def get_notes():
    tmp = {'status': False, 'data':[]}
    try:
        tmp_notes = session.query(Note).limit(4).all()
        for i in tmp_notes:
            tmp_data = i.get_dict()
            tmp_data['author'] = session.query(User).filter(User.uid==i.uid).first().nickName
            tmp['data'].append(tmp_data)
        tmp['status'] = True
        return tmp
    except Exception, e:
        print Exception, e
        return tmp

def get_notes_word(content):
    tmp = {'status': False, 'data': []}
    tmp_wid = get_wid(content)
    if tmp_wid['status']:
        try:
            tmp_notes = session.query(Note).filter(Note.wid==tmp_wid['data']).order_by(Note.nid.desc()).limit(3).all()
            for i in tmp_notes:
                tmp_data = i.get_dict()
                tmp_data['author'] = session.query(User).filter(User.uid==i.uid).first().nickName
                tmp['data'].append(i.get_dict())
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'no such word'
        return tmp

def get_notes_user_word(openId, content):
    tmp = {'status': False, 'data': []}
    tmp_uid = get_uid(openId)
    tmp_wid = get_wid(content)
    if tmp_wid['status'] and tmp_uid['status']:
        try:
            tmp_notes = session.query(Note).filter(Note.wid==tmp_wid['data'] and Note.uid==tmp_uid['data']).all()
            for i in tmp_notes:
                tmp['data'].append(i.get_dict())
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'no such user or word'
        return tmp

def get_notes_user(openId):
    tmp = {'status': False, 'data': []}
    tmp_uid = get_uid(openId)
    if tmp_uid['status']:
        try:
            tmp_notes = session.query(Note).filter(Note.uid==tmp_uid['data']).all()
            for i in tmp_notes:
                tmp['data'].append(i.get_dict())
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'no such word'
        return tmp

def delete_note(nid):
    tmp = {'status': False}
    try:
        tmp_note = session.query(Note).filter(Note.nid==nid).first()
        if tmp_note:
            session.delete(tmp_note)
            session.commit()
            tmp['status'] = True
            return
        else:
            tmp['info'] = 'no such note'
    except Exception, e:
        print Exception, e
        return tmp
