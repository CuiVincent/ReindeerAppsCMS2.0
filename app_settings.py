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
    'template_path': path.join(path.dirname(__file__), 'res/template'),
    # 'listen_ip': None,
    # 'listen_port': 9000
    'listen_ip': os.environ['OPENSHIFT_PYTHON_IP'],
    'listen_port': int(os.environ['OPENSHIFT_PYTHON_PORT'])
}

# app_listen_settings = {
#     'listen_ip': None,
#     'listen_port': 9000
# }

app_listen_settings = {
    'ip': os.environ['OPENSHIFT_PYTHON_IP'],
    'port': int(os.environ['OPENSHIFT_PYTHON_PORT'])
}

# db_settings = {
#     'driven': 'MySQL',
#     'host': '192.168.174.90',
#     'user': 'racms_dba',
#     'password': 'racms_dba',
#     'port': '3306',
#     'database': 'racms'
# }

db_settings = {
    'driven': 'MySQL',
    'host': '127.12.78.130',
    'user': 'adminH8ipecv',
    'password': 'TZ15i4Qpyjj4',
    'port': '3306',
    'database': 'ra'
}
