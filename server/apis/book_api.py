#!/usr/bin/env python
#coding=utf8

from config import *


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
