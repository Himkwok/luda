# -*- coding: utf-8 -*-
from ludaweb.api.apps import App

__version__ = '0.1'
from flask import Flask
from flask_restful import Api, Resource
from celery import Celery

app = Flask('ludaWeb')
app.debug = True

# app.config['CELERY_BROKER_URL'] = 'redis://47.92.37.219:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://47.92.37.219:6379/0'
#
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

# import controllers
from ludaweb.controllers import *

# import model
from ludaweb.models.models import db

#### initial logger ####
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_PATH = '/'.join((os.path.dirname(os.path.realpath(__file__)), 'log'))
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

handler = RotatingFileHandler(LOG_PATH + '/debug.log', maxBytes=10000, backupCount=1)
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
#### initial logger ####


#### initial sesion ####
from datetime import timedelta

app.config['SECRET_KEY'] = 'random'
app.permanent_session_lifetime = timedelta(seconds=60 * 60 * 10)  # session expire time
#### initial sesion ####


#### initial database ####
APP_ROOT = os.path.dirname(os.path.realpath(__file__))

app.config.from_pyfile(os.path.join(APP_ROOT, 'config') + '/database.cfg')
db.init_app(app)
#### initial database ####


#### router ####
from werkzeug.routing import Rule

urlpatterns = [
    Rule('/', endpoint='index'),
    Rule('/widgets', endpoint='widgets'),
    Rule('/applications', endpoint='applications'),
    Rule('/applications/add', endpoint='addapplications'),
    Rule('/applications/save', endpoint='saveapplications'),
    Rule('/qstb/<int:id>', endpoint='qstb'),
    Rule('/mps/webhook', endpoint='webhook', methods=['GET', 'POST']),
]
api = Api(app)
api.add_resource(App, '/api/applications')

for rule in urlpatterns:
    app.url_map.add(rule)
#### router ####
