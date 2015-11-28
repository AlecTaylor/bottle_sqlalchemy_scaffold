from __future__ import absolute_import
from pkg_resources import resource_filename
from json import load
from bottle import Bottle, response, request
from ...utils import depends, sqlalchemy_plugin, Base, engine, has_json, mk_valid_body_mw
from .models import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

api = Bottle()
depends(api, sqlalchemy_plugin(Base))
create_session = sessionmaker(bind=engine)
with open(resource_filename(__name__, 'user_schema.json'), 'rt') as f:
    user_schema = load(f)


@api.post('/user', apply=(has_json, mk_valid_body_mw(user_schema),))
def create():
    session = create_session()
    try:
        user = User(**request.json)
        session.add(user)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        status_code, error_message = {
            'IntegrityError': (422, 'User already exists')
        }.get(e.__class__.__name__, (400, e.message))
        response.status = status_code
        return {'error': e.__class__.__name__,
                'error_message': error_message}
    finally:
        user = locals().get('user')
        if user:
            user = user.to_d()
        session.close()
    response.status = 201
    return user


@api.get('/user/<email>')
def read(email, db):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        response.status = 404
        return {'error': 'NotFound', 'error_message': 'User not found'}

    return {'email': user.email}
