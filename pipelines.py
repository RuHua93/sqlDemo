# coding=utf-8
import sqlite3
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class SqlDemoPipeline(object):

    def __init__(self):
        self.conn = None
        self.filename = "/tmpdb/test.db"
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        # 此处应加判断逻辑,如果更新则检查订阅表
        # if (checkUpdate()):
        #     dealOrder()
        csr = self.conn.cursor()
        csr.execute("select title from sqlDemo where link = ?", (item['link'],))
        recs = csr.fetchall()
        # upd = False
        if len(recs) == 0:
            self.conn.execute("insert into sqlDemo values(?,?,?,?,?,?,?)",
                              (item['title'], item['link'], item['src'], item['time'],
                               item['ctime'], item['rate'], item['rnum']))
            # upd = True
        elif (len(recs[0]) != 0) and (recs[0][0] != item['title']):
            self.conn.execute("update sqlDemo set title = ?, time = ? where\
                              link = ?", (item['title'], item['time'], item['link']))
            # upd = True
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()

            csr = self.conn.cursor()
            csr.execute("select * from sqlDemo")
            recs = csr.fetchall()
            # for rec in recs:
            #     for item in rec:
            #         print "@"+item+"@"
            #     print "############"

            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn=sqlite3.connect(filename)
        conn.execute("""create table sqlDemo(title text, link text, src text,
                    time datetime, ctime datetime, rate numeric, rnum numeric)""")
        conn.commit()
        return conn