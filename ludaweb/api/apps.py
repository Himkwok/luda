from flask import Flask, make_response
from flask_restful import Api, Resource
from ludaweb.models.applications import Application
from ludaweb.models.models import db


class App(Resource):
    def get(self):
        return list(map(lambda x: x.to_json(), Application.query.filter_by(xybz=1).all()))
