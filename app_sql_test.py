##### Example - sqlite3 Interactions #####
## Import libraries
import os
import sqlite3

## Initialize a connection
connection = sqlite3.connect(os.environ.get('DB_CONNECTION')) ## sqltite3 database file: Proper_REST_API_SQL_DB/data.db
cursor = connection.cursor() ## Will execute queries

## Create the users table
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

## Insert a record into the users table
user = (1, 'bob', 'asdf') ## Tuple
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)
connection.commit()

## Insert many records into users table
users = [
    (2, 'JC', 'lala'),
    (3, 'Char','test')
]

cursor.executemany(insert_query, users)
connection.commit()

## Query Data
select_query = "SELECT * FROM users"
query_data = cursor.execute(select_query)

## Close
connection.close()