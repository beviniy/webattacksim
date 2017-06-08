#-*- coding:utf-8 -*-

"""
@created on 2017-06-06
@auther:Ziv Xiao
"""

import json

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


"""数据库ORM映射"""


Base = declarative_base()


session = None      # 数据库的连接session

class Packet(Base):
    """数据库Packet表的映射类"""

    __tablename__ = "packet"        # 表名

    id = Column("id", Integer, primary_key=True)    # 数据库字段
    uname = Column("uname", String(20))
    utype = Column("utype", Integer)
    upath = Column("upath", String(60))

def load_config(config = "dbconfig.json"):
    """从配置文件中获取数据库的连接字符串"""
    
    return "mysql+mysqldb://%(username)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8" \
        % json.load(open(config))

def get_session():      
    """返回session，供外部调用。这样的写法是保证同时只有一个session被初始化，即单例模式"""
    
    global session  # 声明session是全局变量
    if not session:
        connect_string = load_config()
        engine = create_engine(connect_string, echo=False)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
    return session

if __name__ == "__main__":
    
    """测试"""
    
    session = get_session()
    
    for pt in session.query(Packet):
        print pt.id, pt.uname, pt.utype, pt.upath