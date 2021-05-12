# -*- coding: utf-8 -*-
# @Time    : 2021-05-12
# @Author  : hlmio
from u_工具 import *

oracle_conf_a1 = {
    "host": "192.168.1.123",
    "port": 1521,
    "user": "c##admin",
    "password": "admin",
    "db": "orcl"
}

dblink_dict = {
    "a1": oracle_conf_a1,
}



def _get表某些注释(dal, 表名, 用户名=None, dblink=None, 系统注释表='all_col_comments', 表名等值匹配=True):
    if dblink:
        系统注释表 += f"@{dblink}"

    sql = f'''
        select t.*
        from {系统注释表} t
        where 1 = 1
    '''
    if 用户名:
        sql += f" and t.owner = upper('{用户名}') "

    if 表名等值匹配:
        sql += f" and t.table_name = upper('{表名}') "
    else:
        sql += f" and t.table_name like '%'||upper('{表名}')||'%' "

    lines = dal.exec(sql).lines

    # 判断是否出现多张表
    if not 表名等值匹配:
        表名_list = stream(lines).map(lambda i: i["TABLE_NAME"]).collect()
        表名_set = set(表名_list)
        if len(表名_list) != len(表名_set):
            raise Exception("因模糊匹配查找到多张表")

    return lines
def get表字段注释(dal, 表名, 用户名=None, dblink=None, 系统注释表='all_col_comments', 表名等值匹配=True):
    lines = _get表某些注释(dal, 表名, 用户名=用户名, dblink=dblink, 系统注释表=系统注释表, 表名等值匹配=表名等值匹配)
    列名_list = stream(lines).map(lambda i: i["COLUMN_NAME"]).collect()
    注释_list = stream(lines).map(lambda i: i["COMMENTS"]).collect()
    return 列名_list,注释_list
def get表名注释(dal, 表名, 用户名=None, dblink=None, 系统注释表='all_tab_comments', 表名等值匹配=True):
    lines = _get表某些注释(dal, 表名, 用户名=用户名, dblink=dblink, 系统注释表=系统注释表, 表名等值匹配=表名等值匹配)
    表名_list = stream(lines).map(lambda i: i["TABLE_NAME"]).collect()
    注释_list = stream(lines).map(lambda i: i["COMMENTS"]).collect()
    return 表名_list, 注释_list



def _创建表在其他库的视图(dal, 旧表dblink, 旧表用户, 旧表表名, 新表dblink, 新表用户, 新表表名, 系统字段表="all_tab_cols"):
    sql = f'''
        select
            t.column_name, t.data_type
        from 
            {系统字段表}{f"@{旧表dblink}" if 旧表dblink else "" } t
        where
            t.table_name = upper('{旧表表名}')
            {f"and t.owner = upper('{旧表用户}')" if 旧表用户 else ''}
        order by t.column_id
    '''
    lines = dal.exec(sql).lines
    select_sql = ""
    for line in lines:
        列名 = line["COLUMN_NAME"]
        列类型 = line["DATA_TYPE"]
        if 列类型 == "CLOB":
            continue
            # 列名 = f"to_char({列名}) {列名}"  # 不行，还是报 ORA-22992: 无法使用从远程表选择的 LOB 定位器
        select_sql += f", {列名}"
    select_sql = select_sql[1:]

    sql = f'''
        create or replace view {f"{新表用户}." if 新表用户 else ""}{新表表名}
            as
        select {select_sql} from {f"{旧表用户}." if 旧表用户 else ""}{旧表表名}{f"@{旧表dblink}" if 旧表dblink else ""}
    '''
    # print(sql)
    if 新表dblink:
        # 在其他数据库建视图
        新表dal = oracle(dblink_dict[新表dblink])
        新表dal.exec(sql).commit()
    else:
        dal.exec(sql)
def _复制表字段注释(dal, 旧表dblink, 旧表用户, 旧表表名, 新表dblink, 新表用户, 新表表名):
    列名_list,注释_list = get表字段注释(dal, 旧表表名, 用户名=旧表用户, dblink=旧表dblink, 系统注释表='all_col_comments', 表名等值匹配=True)

    if 新表dblink:
        dal = oracle(dblink_dict[新表dblink])

    for (列名, 注释) in zip(列名_list, 注释_list):
        try:
            sql = f'''
                comment on column { f"{新表用户}." if 新表用户 else "" }{新表表名}.{列名} is '{注释}'
            '''
            dal.exec(sql)
        except: print(f"给{新表表名}表的{列名}列加注释异常")

    if 新表dblink:
        dal.commit()
def _复制表名注释(dal, 旧表dblink, 旧表用户, 旧表表名, 新表dblink, 新表用户, 新表表名):
    表名_list,注释_list = get表名注释(dal, 旧表表名, 用户名=旧表用户, dblink=旧表dblink, 系统注释表='all_tab_comments', 表名等值匹配=True)

    if 新表dblink:
        dal = oracle(dblink_dict[新表dblink])

    for (表名, 注释) in zip(表名_list, 注释_list):
        try:
            sql = f'''
                comment on table { f"{新表用户}." if 新表用户 else "" }{新表表名} is '{注释}'
            '''
            dal.exec(sql)
        except: print(f"给{新表表名}表的表名加注释异常")

    if 新表dblink:
        dal.commit()
def cp_view(dal, 旧表dblink, 旧表用户, 旧表表名, 新表dblink, 新表用户, 新表表名):
    _创建表在其他库的视图(dal, 旧表dblink, 旧表用户, 旧表表名, 新表dblink, 新表用户, 新表表名)
    print("1.已建立视图")
    _复制表字段注释(dal, 旧表dblink, 旧表用户, 旧表表名, 新表dblink, 新表用户, 新表表名)
    print("2.已复制字段注释")
    _复制表名注释(dal, 旧表dblink, 旧表用户, 旧表表名, 新表dblink, 新表用户, 新表表名)
    print("3.已复制表名注释")
    pass
