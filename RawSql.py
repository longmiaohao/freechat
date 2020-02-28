from django.db import connections
import django
import os
import base64
import re
os.environ.setdefault('DJANGO_SETTING_MODULE', 'freechat.settings')
django.setup()


class RawSql:
    """Django原生sql操作数据库封装类"""
    __sql = ''
    __database_name = ''

    @staticmethod
    def __doc__():
        """用户使用文档"""
        print("set_sql(sql_str)函数:设置sql参数\n"
              "查询类函数:\n"
              "get_dic(sql_str)函数:输出字典类型的查询结果\n"
              "get_list(sql_str)函数:返回列表型结果\n"
              "更新函数:\n"
              "execute(sql_str):传入sql语句，执行正确返回True，执行错误返回False\n"
              "set_db(self, database_name): 输入database的名字，重新设置操作数据库"
              "get_db(): 获取当前连接数据库")

    def __init__(self, database_name='default', sql=''):
        """构造函数"""
        self.__sql = sql
        self.__database_name = database_name

    def set_db(self, database_name):
        self.__database_name = database_name

    def get_db(self):
        return self.__database_name

    def set_sql(self, sql):
        """set_sql(sql_str)函数:设置sql参数"""
        self.__sql = sql

    def get_json(self, sql='', blob=False):
        """get_json(sql_str)函数"""
        if sql:
            self.__sql = sql
        if not self.__sql:
            return False
        cursor = connections[self.__database_name].cursor()
        cursor.execute(self.__sql)
        columns = [col[0] for col in cursor.description]
        get_sql_data = cursor.fetchall()
        if not get_sql_data:
            return None
        lists = []
        for row in get_sql_data:
            if blob:	# 是否有lob
                row = [r for r in row]	# tuple 转 list
                for idx, b in enumerate(row):
                    if bool(re.search("lob|LOB", str(type(b)))):
                        row[idx] = str(base64.b64encode(b.read()), 'utf-8')
            lists.append(dict(zip(columns, row)))
        result = str(lists).replace('\'', '\"')
        connections.close_all()     # 关闭数据库连接
        return result

    def get_list(self, sql=''):
        """get_list(sql_str)函数"""
        if sql:
            self.__sql = sql
        if not self.__sql:
            print("没有SQL语句传入\n")
            return False
        cursor = connections[self.__database_name].cursor()
        cursor.execute(self.__sql)
        data = cursor.fetchall()
        get_sql_data = []
        list_result = []
        for tuple_var in data:
            for var in tuple_var:
                get_sql_data.append(var)
            list_result += get_sql_data
            get_sql_data.clear()
        connections.close_all()     # 关闭数据库连接
        return list_result

    def excute(self, sql=''):
        """执行增加，删除，修改操作，若成功则返回True, 失败则返回False"""
        if sql:
            self.__sql = sql
        if not self.__sql:
            print("没有SQL语句传入\n")
            return False
        cursor = connections[self.__database_name].cursor()
        try:
            cursor.execute(self.__sql)
            connections.close_all() # 关闭数据库连接
            return True
        except:
            connections[self.__database_name].rollback()
            connections.close_all() # 关闭数据库连接
            return False

    def get_colunms(self, table=''):
        """获取表字段结构函数"""
        if not table:
            print("没有表参数传入\n")
            return False
        sql = "select * from %s where rownum<0" %table
        cursor = connections[self.__database_name].cursor()
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        return columns

    def blob_to_b64(self, blob):
        """二进制转base64函数"""
        return base64.b64encode(blob.read())

