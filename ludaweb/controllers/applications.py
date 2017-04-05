# -*- coding: utf-8 -*-
from ludaweb import app
from ludaweb.models.applications import Application
from ludaweb.models.models import db
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack

from ludaweb.models.params import Param


@app.endpoint('applications')
def index():
    return render_template('applications.html')


@app.endpoint('addapplications')
def add():
    return render_template('applications_add.html')


@app.endpoint('saveapplications')
def save():
    appId = request.form['appId']
    appName = request.form['appName']
    appDes = request.form['appDes']
    appUrl = request.form['appUrl']

    argNames = request.values.getlist('argName')

    argNames = map(lambda x: Param(appId=appId, argName=x), argNames)

    argNames = list(argNames)

    application = Application(appId=appId, appName=appName, appDes=appDes, url=appUrl, xybz=1, args=argNames)

    db.session.add(application)
    try:

        db.session.commit()
    except Exception as err:
        app.logger.error(err)
        db.session.rollback()
        return "fail"
    return "success"
