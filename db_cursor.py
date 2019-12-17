import os,sys
import psycopg2 as db
from flask import flash


def select(columns, table, others=None):
    query = """SELECT {} FROM {}""".format(columns, table)
    if(others != None):
         query += " " + others
    return run(query)

def update(table, columns_values, where):
    query = """UPDATE {} SET {} WHERE {}""".format(table, columns_values, where)
    return run(query)

def delete(table, where):
    query = """DELETE FROM {} WHERE {}""".format(table, where)
    return run(query)

def insert(table,columns,values):
    print("INSERT")
    query = """INSERT INTO {} ({}) VALUES({});""".format(table, columns,values)
    return run(query)

def run(query):
    print("RUN")
    connection = None
    result = None
    try:
        connection = db.connect(os.environ.get('DATABASE_URL'))
        cursor = connection.cursor()
        cursor.execute(query)
        print("db cursor")
        if(not 'DROP' in query and not 'UPDATE' in query and not 'DELETE' in query and not 'INSERT' in query):
            result = cursor.fetchall()
        else:
            result = {"result":1,"message":"Success"}
    except db.DatabaseError as dberror:
        if connection != None:
            connection.rollback()
        result = {"result": -1, "message": dberror}
        flash('Query unsuccessful.', 'danger')
    finally:
        if connection != None:
            connection.commit()
            connection.close()
            cursor.close()
        return result
