# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class SpiderjiakaoPipeline(object):
    def process_item(self, item, spider):
        return item
class MySqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):#这里settings参数可以将settings配置文件传递进来，然后读取里面的数据
#         参数名称要有固定的写法
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        # adbapi可以把mysql操作变成异步操作
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)

    def process_item(self,item,spider):
        #使用twisted把mysql插入变成异步操作
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)#处理异常
        return item

    def handle_error (self,failure):
        #处理异步插入异常
        print(failure)
    def do_insert(self,cursor,item):
        #执行具体操作
        insert_sql = """
                            insert into questions(subject,type,createtime,taotiid,optiona,optionb,optionc,optiond,answer,image_url)
                            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(insert_sql,(item["subject"],item["type"],item["createtime"],item["taotiid"],item["optiona"],item["optionb"],item["optionc"],item["optiond"],item["answer"],item["image_url"],))
        print('导入数据库了')