# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class Bigb2BspiderPipeline(object):
#     def process_item(self, item, spider):
#         return item

import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
import redis
import os
import pymongo

# 爬虫启动时
# checkFile = "isRunning.txt"



class MysqlTwistedPiplines(object):
    def __init__(self,dbpool,settings):
        self.dbpool,self.settings = dbpool,settings
        # self.Rh = _Redis_Help(host='192.168.1.30', db=11)
        # self.pool = redis.ConnectionPool(host='192.168.1.30', port=6379)
        # self.r = redis.Redis(connection_pool=self.pool)
        self.r = redis.Redis(host='192.168.1.30', port=6379, db=11)
        # self.pipe = self.r.pipeline(transaction=True)

    @classmethod
    def from_settings(cls,settings):
        dbparms=dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool,settings)

    def process_item(self, item, spider):
        #使用twisted将mysql插入股变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)#处理异常
        return item

    def handle_error(self, failure,item,spider):
        #处理异步插入的异常
        # 处理mysql断线从链
        if failure.value.args[1] == 'MySQL server has gone away':
            try:
                dbparms = dict(
                    host=self.settings["MYSQL_HOST"],
                    db=self.settings["MYSQL_DBNAME"],
                    user=self.settings["MYSQL_USER"],
                    passwd=self.settings["MYSQL_PASSWORD"],
                    charset="utf8",
                    cursorclass=MySQLdb.cursors.DictCursor,
                    use_unicode=True
                )
                dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
                self.dbpool = dbpool
            except:
                pass
        else:
            print(failure)
            pass

    def do_insert(self,cursor,item):
        insert_sql,params = item.insert_sql()
        result = self.r.sadd("spider_item", item["company_id"])
        if result:
            if params:
                try:
                    cursor.execute(insert_sql,params)
                    print("插入数据成功")
                except:
                    print("数据插入失败")
                    pass
            else:
                print("数据不合法")


class MysqlTwistedPiplines_v1(object):
    def __init__(self,dbpool,settings):
        self.dbpool,self.settings = dbpool,settings
        # self.Rh = _Redis_Help(host='192.168.1.30', db=11)
        # self.pool = redis.ConnectionPool(host='192.168.1.30', port=6379)
        # self.r = redis.Redis(connection_pool=self.pool)
        # self.r = redis.Redis(host='192.168.1.30', port=6379, db=11)
        # self.pipe = self.r.pipeline(transaction=True)

    @classmethod
    def from_settings(cls,settings):
        dbparms=dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool,settings)

    def process_item(self, item, spider):
        #使用twisted将mysql插入股变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)#处理异常
        return item

    def handle_error(self, failure,item,spider):
        #处理异步插入的异常
        # 处理mysql断线从链
        if failure.value.args[1] == 'MySQL server has gone away':
            try:
                dbparms = dict(
                    host=self.settings["MYSQL_HOST"],
                    db=self.settings["MYSQL_DBNAME"],
                    user=self.settings["MYSQL_USER"],
                    passwd=self.settings["MYSQL_PASSWORD"],
                    charset="utf8",
                    cursorclass=MySQLdb.cursors.DictCursor,
                    use_unicode=True
                )
                dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
                self.dbpool = dbpool
            except:
                pass
        else:
            print(failure)
            pass

    def do_insert(self,cursor,item):
        insert_sql,params = item.insert_sql()
        # result = self.r.sadd("spider_item", item["company_id"])
        # if result:
        if params:
            try:
                cursor.execute(insert_sql,params)
                print("插入数据成功")
            except:
                print("数据插入失败")
                pass
        else:
            print("数据不合法")

# MongoPipeline
# class MongoPipeline(object):
#     collection_name='scrapy_items'
#     def __init__(self,mongo_uri,mongo_db,collection_name):
#         self.mongo_uri=mongo_uri
#         self.mongo_db=mongo_db
#         self.collection_name = collection_name
#         #需要在setting中配置
#         # #MONGO_URI="127.0.0.1:27017"
#         # #MONGO_DATABASE="spider"
#     @classmethod
#     def from_crawler(cls,crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE','items'),
#             collection_name=crawler.settings.get('COLLECTION_NAME'))
#
#     def open_spider(self,spider):
#         self.client=pymongo.MongoClient(self.mongo_uri) # 连接Mongodb
#         self.db=self.client[self.mongo_db] # 待存储数据的数据库mydata
#         self.collection = self.collection_name  # 表名
#         f = open(checkFile, "w")  # 创建一个文件，代表爬虫在运行中
#         f.close()
#
#     def close_spider(self,spider):
#         self.client.close()
#         isFileExsit = os.path.isfile(checkFile)
#         if isFileExsit:
#             os.remove(checkFile)
#
#     def process_item(self,item,spider):
#         self.db[self.collection].insert(dict(item))
#         return item