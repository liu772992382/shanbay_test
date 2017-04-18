# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Table, Text, \
                       text, create_engine, Boolean, extract, and_, or_, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from flask import Flask
from config import *
import sys, os
import time
from datetime import datetime

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker()
Session.configure(bind=engine)
Base = declarative_base()
session = Session()




class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True) #用户编号
    openId = Column(String(255))    #微信openId
    # userName = Column(String(255), unique=True)  #用户名
    # passWord = Column(String(255))  #密码hash值
    nickName = Column(String(30))  #昵称
    gender = Column(Integer)    #性别
    # type = Column(Integer, default = 1)  #用户类型，具体类型待定
    loginTime = Column(String(30)) #用户上次登陆时间
    avatarUrl = Column(String(255))    #用户头像链接
    city = Column(String(30))  #所在城市
    createTime = Column(DateTime(timezone=True), default=datetime.today())    #用户创建时间
    enLevel = Column(Integer, default=0) #用户英语水平
    task = Column(Integer, default=50)    #用户每日背单词数
    isDel = Column(Boolean, default=False)  #用户逻辑删除标识

# , default=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def init_user(self, kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

# class UserBook(Base):
#     __tablename__ = 'user_book'
#
#     ubid = Column(Integer, primary_key=True)
#     bid = Column(ForeignKey(u'books.bid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #单词书编号
#     uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #用户编号
#     choose = Column(Boolean, default=False)    #单词书当前是否被选中
#
#     book = relationship(u'Book')
#     user = relationship(u'User')


class Word(Base):
    __tablename__ = 'words'

    wid = Column(Integer, primary_key=True) #单词编号
    content = Column(String(30), nullable=False, unique=True)    #单词内容
    definition = Column(String(255))    #单词释义
    example = Column(String(255))   #单词例句
    pron = Column(String(255)) #单词音标

    def init_word(self, kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

class Book(Base):
    __tablename__ = 'books'

    bid = Column(Integer, primary_key=True) #单词书编号
    name = Column(String(50))   #单词书名
    createTime = Column(DateTime(timezone=True), default=datetime.today())    #创建时间

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__


class WordBook(Base):
    __tablename__ = 'word_book' #单词与单词书的关系列表

    wbid = Column(Integer, primary_key=True)    #关系编号
    wid = Column(ForeignKey(u'words.wid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #单词编号
    bid = Column(ForeignKey(u'books.bid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #单词书编号

    book = relationship(u'Book')
    word = relationship(u'Word')


class Task(Base):
    __tablename__ = 'tasks'

    tid = Column(Integer, primary_key=True) #任务编号
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #任务用户编号
    wid = Column(ForeignKey(u'words.wid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #单词编号
    bid = Column(ForeignKey(u'books.bid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    date = Column(Date, default=datetime.today().date())  #任务日期
    status = Column(Integer, default=0)    #任务状态，0为当日未完成，1为完成


    user = relationship(u'User')
    word = relationship(u'Word')
    book = relationship(u'Book')

    def init_task(self, kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

class Check(Base):
    __tablename__ = 'checks'

    cid = Column(Integer, primary_key=True)
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #任务用户编号
    status = Column(Integer, default=0) #当日任务状态，0表示未设置，1表示已设置但未完成， 2表示当日已完成
    date = Column(Date, default=datetime.today().date())   #创建日期

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__


class Note(Base):
    __tablename__ = 'notes'

    nid = Column(Integer, primary_key=True) #笔记编号
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #笔记用户编号
    content = Column(String(255))   #笔记内容
    wid = Column(ForeignKey(u'words.wid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #单词编号
    createTime = Column(DateTime(timezone=True), default=datetime.today())    #创建时间

    user = relationship(u'User')
    word = relationship(u'Word')

    def init_note(self, kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__
