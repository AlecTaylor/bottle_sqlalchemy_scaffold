from __future__ import absolute_import
from bottle import Bottle, response, request
from bottle_sqlalchemy_scaffold.utils import depends, sqlalchemy_plugin, Base, engine
from bottle_sqlalchemy_scaffold.api.user.models import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from psycopg2 import IntegrityError

api = Bottle()
depends(api, sqlalchemy_plugin(Base))
create_session = sessionmaker(bind=engine)


@api.post('/user')
def create(db):
    session = create_session()
    try:
        user = User(**request.json)
        db.add(user)
        session.commit()
    except SQLAlchemyError as e:
        print('ROLLING BACK')
        session.rollback()
        return {'error': e.__class__.__name__,
                'error_message': 'User already exists'}
    except IntegrityError as e:
        response.status = 422
        return {'error': e.__class__.__name__,
                'error_message': 'User already exists'}
    except Exception as e:
        if e.__class__.__name__ == 'IntegrityError':
            response.status = 422
        return {'error': e.__class__.__name__,
                'error_message': 'User already exists'}
    finally:
        print('closing session')
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
