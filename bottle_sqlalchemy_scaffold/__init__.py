#!/usr/bin/env python

from __future__ import absolute_import
from os import environ
from bottle import Bottle
from utils import depends, sqlalchemy_plugin, Base
from bottle_sqlalchemy_scaffold.api.user.routes import api as user_api

__author__ = 'Samuel Marks'
__version__ = '0.0.1'

api = Bottle()
api.merge(user_api)
depends(api, sqlalchemy_plugin(Base))

if __name__ == '__main__':
    api.run(port=int(environ.get('PORT', '3333')))
