#-*- coding:utf-8 -*-

"""
@created on 2017-06-06
@auther:Ziv Xiao
"""

import json

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


session = None

class Packet(Base):

    __tablename__ = "packet"

    id = Column("id", Integer, primary_key=True)
    uname = Column("uname", String(20))
    utype = Column("utype", Integer)
    upath = Column("upath", String(60))

def load_config(config = "dbconfig.json"):
    return "mysql+mysqldb://%(username)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8" \
        % json.load(open(config))

def get_session():
    global session
    if not session:
        connect_string = load_config()
        engine = create_engine(connect_string, echo=False)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
    return session

if __name__ == "__main__":
    
    session = get_session()
    
    for pt in session.query(Packet):
        print pt.id, pt.uname, pt.utype, pt.upath