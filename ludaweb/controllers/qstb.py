# -*- coding: utf-8 -*-
import requests
from flask_celery import single_instance

from ludaweb import app
from ludaweb.models.applications import Application
from ludaweb.models.models import db
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack, jsonify

from ludaweb.models.params import Param
from ludaweb.models.applications import Application
from ludaweb.models.models import db

from ludaweb.cron.celerywork import *


@app.endpoint('qstb')
def index(id):
    # id = request.args.get('id')

    app = Application.query.filter_by(id=id).first()
    # print(app.url)
    ret = requests.post(app.url, data={})
    returnList = ret.json()['result']

    # for apps in returnList:
    #     print(apps)
    return render_template('qstb.html', datalist=returnList)
