# -*- coding: utf-8 -*-

from ludaweb import app
from flask import Flask, request, session, url_for, redirect,  render_template, abort, g, flash, _app_ctx_stack


from ludaweb.models.models import db
from ludaweb.models.user import User


@app.endpoint('index')
def index():
    return render_template('index.html')