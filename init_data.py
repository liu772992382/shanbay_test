# coding: utf-8
from model import *

fileName = '6.txt'

def create_word(content, bid):
    try:
        tmp_word = session.query(Word).filter_by(content=content).first()
        # if not tmp:
        #     tmp_word = Word()
        #     tmp_word.content = content
        #     session.add(tmp_word)
        #     session.commit()
        tmp_word_book = WordBook()
        tmp_word_book.bid = bid
        tmp_word_book.wid = tmp_word.wid
        session.add(tmp_word_book)
        session.commit()
    except Exception, e:
        print Exception, e

with open(fileName) as f:
    tmp_book_bid = session.query(Book).filter_by(name="6级词汇").first().bid
    print tmp_book_bid
    for i in f.readlines():
        if i.split() != []:
            # print i.split()[0]
            # print i.strip()
            # create_word(i.strip()[1:], tmp_book_bid)
            create_word(i.split('\xe3\x80\x80')[0], tmp_book_bid)
            # print i.split('\xe3\x80\x80')
