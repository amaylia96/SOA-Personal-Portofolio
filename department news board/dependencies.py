from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import json

class DatabaseWrapper:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    def doLogin(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append(row['id']),
            result.append(row['username']),
            result.append(row['password'])

        if cursor.rowcount > 0:
            result.append("success")
        else:
            result.append("failed")

        cursor.close()
        return result

    def getAllNews(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM news"
        cursor.execute(sql)
        for row in cursor.fetchall():
            tmp = {
                'id': row['id'],
                'judul': row['judul'],
                'isi': row['isi'],
                'author': row['author'],
                'file': row['file'],
                'created_at': row['created_at']
            }

            result.append(tmp)
        cursor.close()
        return result

    def getNewsById(self, id):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM news WHERE id='{}'".format(id)
        cursor.execute(sql)
        for row in cursor.fetchall():
            tmp = {
                'id': row['id'],
                'judul': row['judul'],
                'isi': row['isi'],
                'author': row['author'],
                'file': row['file'],
                'created_at': row['created_at']
            }

            result.append(tmp)
        cursor.close()
        return result

    def downloadFileById(self, id):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM news WHERE id='{}'".format(id)
        cursor.execute(sql)
        file = ''
        for row in cursor.fetchall():
            file = row['file']
            break

        cursor.close()
        return file

    def addNews(self, judul, isi, author, file):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "INSERT INTO news (judul, isi, author, file) VALUES ('"+ judul +"', '"+ isi +"', '"+ author +"', '"+ file +"')"
        cursor.execute(sql)
        cursor.close()
        self.connection.commit()
        return "add news created successfully"
        
    def editNews(self, idnews, judul, isi):
        if judul:
            sql = "UPDATE news SET judul = '" + judul + "' WHERE id = " + idnews
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(sql)
            cursor.close()
            self.connection.commit()

        if isi:
            sql = "UPDATE news SET isi = '" + isi + "' WHERE id = " + idnews
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(sql)
            cursor.close()
            self.connection.commit()

        return "edit news created successfully"

    def deleteNews(self, idnews):
        cursor = self.connection.cursor(dictionary=True)
        sql = "DELETE from news WHERE id='{}'".format(idnews)
        cursor.execute(sql)
        cursor.close()
        self.connection.commit()
        return "news deleted successfully"

    def getUser(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM users WHERE username = %s and password = %s; """, (username, password))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'username': row['username']
            })
            
        cursor.close()
        return result


class Database(DependencyProvider):
    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='cloud_storage',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
