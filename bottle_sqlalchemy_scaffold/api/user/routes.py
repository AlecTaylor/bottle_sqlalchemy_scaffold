from __future__ import absolute_import
from bottle import Bottle, response, request
from ...utils import depends, sqlalchemy_plugin, Base, engine
from .models import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

api = Bottle()
depends(api, sqlalchemy_plugin(Base))
create_session = sessionmaker(bind=engine)


@api.post('/user')
def create():
    session = create_session()
    try:
        user = User(**request.json)
        session.add(user)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        response.status = 422
        return {'error': e.__class__.__name__,
                'error_message': 'User already exists'}
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
    if user:
        return {'email': user.email}
    response.status = 404
    return {'error': 'NotFound', 'error_message': 'User not found'}
