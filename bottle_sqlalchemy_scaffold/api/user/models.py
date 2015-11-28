from bottle_sqlalchemy_scaffold.utils import Base
from sqlalchemy import Column, Integer, Sequence, String


class User(Base):
    __tablename__ = 'user_tbl'
    __table_args__ = {'extend_existing': True}

    email = Column(String, primary_key=True)
    password = Column(String)

    def __repr__(self):
        return "<User('{email}')>".format(email=self.email)
