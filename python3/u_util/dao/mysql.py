# coding:utf-8

import pymysql

mysql_conf = {
    "host": "106.13.231.168",
    "port": 3306,
    "user": "root",
    "password": "ans573KUR",
    "db": "test",
    "charset": "utf8"
}

def get_mysql_conf(new_conf={}):
    # if not new_conf:
    #     return copy.deepcopy(_mysql_conf)
    conf = {}
    conf["host"] = new_conf.get("host", mysql_conf["host"])
    conf["port"] = new_conf.get("port", mysql_conf["port"])
    conf["user"] = new_conf.get("user", mysql_conf["user"])
    conf["password"] = new_conf.get("password", mysql_conf["password"])
    conf["db"] = new_conf.get("db", mysql_conf["db"])
    conf["charset"] = new_conf.get("charset", mysql_conf["charset"])
    return conf

class Mysql:
    def __init__(self, conf=mysql_conf):
        self.conn = pymysql.connect(host=conf["host"], port=conf["port"], user=conf["user"], password=conf["password"],
                                    db=conf["db"], charset=conf["charset"])
        self.cursor = self.conn.cursor()

        self.count = 0
        self.rows = []
        self.lines = []

        self.conn.autocommit(True)

    def __del__(self):
        if self.conn:
            try:
                self.conn.close()
            except:
                pass

    @staticmethod
    def 实例化(new_conf={}):
        conf = get_mysql_conf(new_conf)
        return Mysql(conf)

    def exec(self, sql: str, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.rows = self.cursor.fetchall()
        self.lines = self._rows_to_lines(self.rows, self.cursor)
        self.count = self.cursor.rowcount
        return self

    def call(self, proc_name: str, params=[]):
        self.cursor.callproc(proc_name, params)
        self.rows = self.cursor.fetchall()
        self.lines = self._rows_to_lines(self.rows, self.cursor)
        self.count = self.cursor.rowcount
        if params:
            select_params = ",".join([f'@_{proc_name}_{i}' for i in range(len(params))])
            self.cursor.execute(f"select {select_params}")
            in_out = self.cursor.fetchone()
            for i in range(len(params)):
                params[i] = in_out[i]
        return self

    def begin(self):
        self.conn.begin()
        return self

    def commit(self):
        self.conn.commit()
        return self

    def rollback(self):
        self.conn.rollback()
        return self

    def _rows_to_lines(self, rows, cursor):
        try:
            # col_names = stream(self.cursor.description).map(lambda c: c[0]).collect()
            col_names = [c[0] for c in cursor.description]
        except:
            pass
        lines = []
        for row in rows:
            r_dict = {}
            for i, col in enumerate(row):
                r_dict[col_names[i]] = col
            lines.append(r_dict)
        return lines

def mysql(new_conf={}):
    return Mysql.实例化(new_conf)
