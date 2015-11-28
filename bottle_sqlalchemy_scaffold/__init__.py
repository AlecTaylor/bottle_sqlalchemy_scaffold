#!/usr/bin/env python

__author__ = 'Samuel Marks'
__version__ = '0.0.1'

from os import environ
from bottle import Bottle
from utils import depends, sqlalchemy_plugin, Base
from api.user.routes import api as user_api

api = Bottle()
api.merge(user_api)
depends(api, sqlalchemy_plugin(Base))

if __name__ == '__main__':
    api.run(port=int(environ.get('PORT', '3333')))
