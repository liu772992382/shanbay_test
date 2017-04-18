#!/usr/bin/env python
#coding=utf8

from apis.book_api import *
from apis.note_api import *
from apis.task_api import *
from apis.user_api import *
from apis.word_api import *

if __name__ == '__main__':
    app.run(debug=True, port=HOST_PORT, host='0.0.0.0')
