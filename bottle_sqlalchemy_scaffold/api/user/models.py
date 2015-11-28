from __future__ import absolute_import
from ...utils import Base
from sqlalchemy import Column, String


class User(Base):
    __tablename__ = 'user_tbl'

    email = Column(String, primary_key=True)
    password = Column(String)

    def __repr__(self):
        return "<User('{email}')>".format(email=self.email)

    def to_d(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
