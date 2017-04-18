#!/usr/bin/env python
#coding=utf8

from config import *

#-----------------------单词接口-------------------------------------------
@app.route('/shanbay/word/get/<string:name>', methods=['GET'])
def word_get(content):
    return jsonify(get_word(name))

@app.route('/shanbay/word/create', methods=['POST'])
def word_create():
    tmp_data = request.get('word_data')
    return jsonify(create_word(word_data))

# @app.route('/shanbay/word/delete/<string:content>', methods=['GET'])
# def word_delete(content):
#     return jsonify(delete_word(content))
