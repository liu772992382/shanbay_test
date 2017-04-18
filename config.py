#!/usr/bin/env python
#coding=utf-8
from os import urandom

SQLALCHEMY_DATABASE_URI='mysql://root:19951028liu@localhost:3306/shanbay_test?charset=utf8'
SQLALCHEMY_COMMIT_ON_TEARDOWN=True
SQLALCHEMY_TRACK_MODIFICATIONS=True
SECRET_KEY = 'Shanbay'
#admin
# ADMIN_USERNAME = 'Shanbay_test'
# ADMIN_PASSWORD = 'ShanbayAdmin'

HOST_PORT = 8082
