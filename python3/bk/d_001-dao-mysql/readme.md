## 使用方法
1.新建连接

    dal = mysql()
    
2.执行sql语句

    sql = f'''
        SELECT * FROM a1
    '''
    dal.exec(sql)
    
3.获取查询的行

    dal.rows   # 元组结果
    dal.lines  # 字典结果
    
<br/>注：自动提交我默认开了


<br/>

## [详细介绍](https://blog.csdn.net/u013595395/article/details/108911475)
