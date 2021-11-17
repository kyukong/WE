from flask import g
import pymysql
from app.config import DB


def connect():
    if hasattr(g, 'conn'):
        return

    conn = pymysql.connect(
        host=DB['host'], 
        port=DB['port'], 
        user=DB['user_id'], 
        password=DB['user_pw'], 
        database=DB['database'], 
        charset=DB['charset'])

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    g.conn = conn
    g.cursor = cursor


def commit():
    conn = g.conn
    conn.commit()


def rollback():
    conn = g.conn
    conn.rollback()


def close():
    if hasattr(g, "conn"):
        conn = getattr(g, "conn")
        conn.close()
        delattr(g, 'conn')


def select(sql):
    result = dict()
    result['result'] = 'fail'
    try:
        connect()
        cursor = g.cursor
        cursor.execute(sql)

        db_result = cursor.fetchall()
        
        result['result'] = 'success'
        result['data'] = db_result
        result['count'] = len(result['data'])    
    except Exception as ex:
        result['data'] = ex
        result['count'] = 0
    finally:
        return result


def insert(sql):
    result = dict()
    result['result'] = 'fail'
    try:
        connect()
        cursor = g.cursor

        sql_list = sql.split(";")
        for sql_info in sql_list:
            if sql_info == "" or sql_info == " ":
                continue
            
            cursor.execute(sql_info.strip())

        db_result = cursor.rowcount

        if db_result > 0:
            result['result'] = 'success'
        result['data'] = db_result
        result['count'] = db_result
    except Exception as ex:
        rollback()

        result['data'] = ex
        result['count'] = 0
    finally:
        if result['result'] == 'fail':
            rollback()
        return result


def update(sql):
    result = dict()
    result['result'] = 'fail'
    try:
        connect()
        cursor = g.cursor
        
        sql_list = sql.split(";")
        for sql_info in sql_list:
            if sql_info == "" or sql_info == " ":
                continue
            
            cursor.execute(sql_info.strip())

        db_result = cursor.rowcount

        if db_result > 0:
            result['result'] = 'success'
        result['data'] = db_result
        result['count'] = db_result
    except Exception as ex:
        rollback()
        
        result['data'] = ex
        result['count'] = 0
    finally:
        if result['result'] == 'fail':
            rollback()
        return result


def delete(sql):
    result = dict()
    result['result'] = 'fail'
    try:
        connect()
        cursor = g.cursor
        
        sql_list = sql.split(";")
        for sql_info in sql_list:
            if sql_info == "" or sql_info == " ":
                continue
            
            cursor.execute(sql_info.strip())

        db_result = cursor.rowcount

        if db_result > 0:
            result['result'] = 'success'
        result['data'] = db_result
        result['count'] = db_result
    except Exception as ex:
        rollback()
        
        result['data'] = ex
        result['count'] = 0
    finally:
        if result['result'] == 'fail':
            rollback()
        return result
