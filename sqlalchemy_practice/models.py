from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType
import uuid
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'User'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid1)
    name = Column(String(30))
    surname = Column(String(30))