# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Table, Text, \
                       text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask import Flask
from config import *
import sys, os
import time

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker()
Session.configure(bind=engine)
Base = declarative_base()
session = Session()

def get_time():
    return time.strftime("%Y-%m-%d %X", time.localtime())



class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True) #用户编号
    openId = Column(String(255))    #微信openId
    nickName = Column(String(30))  #昵称
    gender = Column(Integer)    #性别
    # type = Column(Integer, default = 1)  #用户类型，具体类型待定
    loginTime = Column(String(30)) #用户上次登陆时间
    avatarUrl = Column(String(255))    #用户头像链接
    city = Column(String(20))  #所在城市
    createTime = Column(String(255))    #用户创建时间
    enLevel = Column(Integer, default = 0) #用户英语水平
    task = Column(Integer, default = 50)    #用户每日背单词数
    restTask = Column(Integer, default = 0) #用户每日剩余单词数

    def init_user(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__



class Word(Base):
    __tablename__ = 'words'

    wid = Column(Integer, primary_key=True) #单词编号
    content = Column(String(30), nullable=False, unique=True)    #单词内容
    definition = Column(String(255))    #单词释义
    example = Column(String(255))   #单词例句
    pron = Column(String(255)) #单词音标

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

class Book(Base):
    __tablename__ = 'books'

    bid = Column(Integer, primary_key=True)
    name = Column(String(50))
    createTime = Column(String(255))

class WordBook(Base):
    __tablename__ = 'word_book'

    wbid = Column(Integer, primary_key=True)
    wid = Column(ForeignKey(u'words.wid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #单词编号
    bid = Column(ForeignKey(u'books.bid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #单词编号

    book = relationship(u'Book')
    word = relationship(u'Word')


class Task(Base):
    __tablename__ = 'tasks'

    tid = Column(Integer, primary_key=True) #用户编号
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #笔记用户编号
    wid = Column(ForeignKey(u'words.wid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #单词编号
    date = Column(String(255))
    status = Column(Integer)


    user = relationship(u'User')
    word = relationship(u'Word')

    def init_user(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

class Note(Base):
    __tablename__ = 'notes'

    nid = Column(Integer, primary_key=True) #用户编号
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #笔记用户编号
    content = Column(String(255))   #笔记内容
    wid = Column(ForeignKey(u'words.wid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #单词编号
    createTime = Column(String(255))

    user = relationship(u'User')
    word = relationship(u'Word')

    def init_user(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__
