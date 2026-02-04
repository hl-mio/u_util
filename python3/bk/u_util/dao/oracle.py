# coding:utf-8

import os
import cx_Oracle

# select userenv('language') from dual;
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'

oracle_conf = {
    "host": "192.168.15.132",
    "port": 1521,
    "user": "c##dba",
    "password": "oracle",
    "db": "orcl"
}

def get_oracle_conf(new_conf={}):
    conf = {}
    conf["host"] = new_conf.get("host", oracle_conf["host"])
    conf["port"] = new_conf.get("port", oracle_conf["port"])
    conf["user"] = new_conf.get("user", oracle_conf["user"])
    conf["password"] = new_conf.get("password", oracle_conf["password"])
    conf["db"] = new_conf.get("db", oracle_conf["db"])
    return f'{conf["user"]}/{conf["password"]}@{conf["host"]}:{conf["port"]}/{conf["db"]}'

class Oracle:
    def __init__(self, conf=get_oracle_conf()):
        self.conn = cx_Oracle.connect(conf)
        self.cursor = self.conn.cursor()

        self.count = 0
        self.rows = []
        self.lines = []

    def __del__(self):
        if self.conn:
            try:
                self.conn.close()
            except:
                pass

    @staticmethod
    def 实例化(new_conf={}):
        conf = get_oracle_conf(new_conf)
        return Oracle(conf)

    def exec(self, sql: str, params=None):
        if params:
            cursor = self.cursor.execute(sql, params)
        else:
            cursor = self.cursor.execute(sql)

        if cursor:
            cursor = self.cursor
            self.rows = cursor.fetchall()
            self.lines = self._rows_to_lines(self.rows, cursor)
            self.count = cursor.rowcount
        else:
            self.rows = ()
            self.lines = {}
            self.count = 0
        return self

    def call(self, proc_name: str, params=[]):
        in_out = self.cursor.callproc(proc_name, params)
        cur_index = -1;
        for i in range(len(params)):
            params[i] = in_out[i]
            if repr(type(in_out[i])) == "<class 'cx_Oracle.Cursor'>":
                cur_index = i

        if cur_index != -1 and in_out[i]:
            cursor = in_out[i]
            self.rows = cursor.fetchall()
            self.lines = self._rows_to_lines(self.rows, cursor)
            self.count = cursor.rowcount
        else:
            self.rows = ()
            self.lines = {}
            self.count = 0

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

def oracle(new_conf={}):
    return Oracle.实例化(new_conf)
