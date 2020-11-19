## Import libraries
import sqlite3

## Database Class
class Database(object):

    @staticmethod
    def connect_to_db():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        return connection, cursor

    @staticmethod
    def close_connection_to_db(conn):
        conn.commit()
        conn.close()
