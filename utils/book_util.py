#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *

def get_bid(name):
    tmp = {'status': False}
    tmp_book = session.query(Book).filter(Book.name==name).first()
    if tmp_book:
        tmp['data'] = tmp_book.bid
        tmp['status'] = True
        return tmp
    else:
        tmp['info'] = 'no such book'
        return tmp


def create_book(name):
    tmp = {'status': False}
    tmp_book = session.query(Book).filter(Book.name==name).first()
    if not tmp_book:
        try:
            tmp_book = Book()
            tmp_book.name = name
            session.add(tmp_book)
            session.commit()
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'this name is existed'
        return tmp

def update_book(name):
    tmp = {'status': False}
    tmp_book = session.query(Book).filter(Book.name==name).first()
    if tmp_book:
        tmp_book.name = name
        tmp['status'] = True
        return tmp
    else:
        tmp['info'] = 'no such book'
        return tmp

def set_wrodBook(words, name):
    tmp = {'status': False}
    tmp_book = session.query(Book).filter(Book.name==name).first()
    if tmp_book:
        try:
            for i in words:
                tmp_word = session.query(Word).filter(Word.content==i.content).first()
                if not tmp_word:
                    tmp_word = Word()
                    tmp_word.init_word(i)
                    session.add(tmp_word)
                    session.commit()
                tmp_word_book = WordBook()
                tmp_word_book.wid = tmp_word.wid
                tmp_word_book.bid = tmp_book.bid
                session.add(tmp_word_book)
                session.commit()
            tmp['status'] = True
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'no such book'
        return tmp

def delete_book(bid):
    tmp = {'status': False}
    tmp_book = session.query(Book).filter(Book.bid==bid).first()
    if tmp_book:
        try:
            session.delete(tmp_book)
            session.commit()
            tmp['status'] = True
            return tmp
        except Exception, e:
            print Exception, e
            return tmp
    else:
        tmp['info'] = 'no such book'
        return tmp

# def create_userBook(openId, name):
#     tmp = {'status': False}
#     tmp_uid = get_uid(openId)
#     tmp_bid = get_bid(name)
#     if tmp_uid['status'] and tmp_bid['status']:
#         try:
#             tmp_user_book = UserBook()
#             tmp_user_book.uid = tmp_uid['data']
#             tmp_user_book.bid = tmp_bid['data']
#             tmp_user_book.choose = True
#             session.add(tmp_user_book)
#             session.commit()
#         except Exception, e:
#             print Exception, e
#             return tmp
#     else:
#         tmp['info'] = 'no such user or book'
#         return tmp
#
# def choose_userBook(openId, name):
#     tmp = {'status': False}
#     tmp_uid = get_uid(openId)
#     tmp_bid = get_bid(name)
#     if tmp_uid['status'] and tmp_bid['status']:
#         tmp_user_book = session.query(UserBook).filter(UserBook.uid==tmp_uid['data'] and UserBook.bid==tmp_bid['data']).first()
#         if tmp_user_book:
#             tmp_user_book.choose = True
#             session.commit()
#             tmp['status'] = True
#             return tmp
#         else:
#             tmp['info'] = "this user did not choose this book"
#             return tmp
#     else:
#         tmp['info'] = 'no such user or book'
#         return tmp
