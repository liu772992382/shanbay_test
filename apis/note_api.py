#!/usr/bin/env python
#coding=utf8

from config import *


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
