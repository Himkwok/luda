from ludaweb import app
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack


@app.endpoint('applications')
def index():
    return render_template('applications.html')


@app.endpoint('addapplications')
def add():
    return render_template('applications_add.html')
