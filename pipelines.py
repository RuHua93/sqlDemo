# coding=utf-8
import sqlite3
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from funcs import sendEmail


class SqlDemoPipeline(object):

    def __init__(self):
        self.conn = None
        self.filename = "/tmpdb/newdb.db"
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        # 此处应加判断逻辑,如果更新则检查订阅表
        # if (checkUpdate()):
        #     dealOrder()
        csr = self.conn.cursor()
        self.conn.row_factory=sqlite3.Row
        csr.execute("select title from sqlDemo where link = ?", (item['link'],))
        recs = csr.fetchall()
        upd = False
        # 第一次加入数据库
        img = "http://center.blueidea.com/avatar.php?uid=291426&size=small"
        if len(recs) == 0:
            self.conn.execute("insert into sqlDemo(title, link, src, img, time, ctime, rate, rnum) values(?,?,?,?,?,?,?,?)",
                              (item['title'], item['link'], item['src'], img, item['ctime'],
                               item['ctime'], item['rate'], item['rnum']))
            # upd = True
        # 更新数据库
        elif (len(recs[0]) != 0) and (recs[0][0] != item['title']):
            self.conn.execute("update sqlDemo set title = ?, time = ? where\
                              link = ?", (item['title'], item['time'], item['link']))
            upd = True

        if upd == True:
            csr.execute("select email from user, od, sqlDemo where od.did=sqlDemo.did and user.uid=od.uid and sqlDemo.link=?", (item["link"],))
            recs = csr.fetchall()
            for rec in recs:
                print "######################"
                print "######################"
                print "######################"
                print "######################"
                print rec["email"]
                sendEmail(item, rec["email"])

        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn=sqlite3.connect(filename)
        conn.execute("""create table sqlDemo(did integer primary key autoincrement, title text, link text, src text, img text, time datetime, ctime datetime, rate numeric, rnum numeric);""")
        conn.commit()
        return conn