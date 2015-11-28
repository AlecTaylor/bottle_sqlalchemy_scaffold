from __future__ import absolute_import
from os import environ
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(environ.get('RDBMS_URI', 'sqlite:///:memory:'), echo=True)

def sqlalchemy_plugin(Base):
    """ Default arguments for sql_alchemy """
    return sqlalchemy.Plugin(
        engine, Base.metadata,
        keyword='db', create=True,
        commit=True, use_kwargs=False
    )


def depends(api, *plugins):
    """
    Installs all plugins which haven't been installed

    :argument api :type bottle.Bottle
    :argument plugins :type {setup: Function} | Function | {apply: Function}

    :returns names of plugins that were installed :type frozenset
    """

    installed = frozenset(plugin.name for plugin in api.plugins)
    return frozenset(plugin.name for plugin in plugins if plugin.name not in installed and api.install(plugin))
