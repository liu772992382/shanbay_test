#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *

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

def set_wrodBook(words, bid):
    tmp = {'status': False}
    tmp_book = session.query(Book).filter(Book.bid==bid).first()
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
