__author__ = 'CuiVincent'
# encoding:utf-8

import os
import base64
import uuid
from os import path


app_settings = {
    'debug': False,
    'cookie_secret': base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
    'login_url': r'/login',
    'xsrf_cookies': True,
    'static_path': path.join(path.dirname(__file__), 'res/static'),
    'template_path': path.join(path.dirname(__file__), 'res/template')
}

use_open_shift = False

if use_open_shift:
    app_listen_settings = {
        'ip': os.environ['OPENSHIFT_PYTHON_IP'],
        'port': int(os.environ['OPENSHIFT_PYTHON_PORT'])
    }

    db_settings = {
        'driven': 'MySQL',
        'host': os.environ['OPENSHIFT_MYSQL_DB_HOST'],
        'user': 'adminH8ipecv',
        'password': 'TZ15i4Qpyjj4',
        'port': os.environ['OPENSHIFT_MYSQL_DB_PORT'],
        'database': 'ra'
    }
else:
    app_listen_settings = {
        'ip': None,
        'port': 9000
    }

    db_settings = {
        'driven': 'MySQL',
        'host': '192.168.174.90',
        'user': 'racms_dba',
        'password': 'racms_dba',
        'port': '3306',
        'database': 'racms'
    }


