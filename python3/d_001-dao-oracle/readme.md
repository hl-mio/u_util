## 使用方法
cx_Oracle版本 7.3

<br/>

1.新建连接

    dal = oracle()
    
2.执行sql语句

    sql = f'''
        SELECT * FROM a1
    '''
    dal.exec(sql).commit()
    
3.获取查询的行

    dal.rows   # 元组结果
    dal.lines  # 字典结果
    
<br/>注：要手动commit()


<br/>

## [详细介绍](https://blog.csdn.net/u013595395/article/details/108924071)
