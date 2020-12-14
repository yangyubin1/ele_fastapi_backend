"""
集中管理中间件（数据库连接、代理，缓存，消息队列等等），以防止循环依赖。
"""

import pymongo
# from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# redis_client = Redis.from_url(settings.REDIS_URL)


class MongoClient():
    def __init__(self, host='localhost', port=27017, database='elm', collection=''):
        self.host = host
        self.port = port
        self.database = database
        self.collection = collection
        self.mongo_client = pymongo.MongoClient(host=self.host, port=self.port)
        link = self.mongo_client[database]
        self.db = link[self.collection]

    def query(self):
        pass

    def close(self):
        self.mongo_client.close()
