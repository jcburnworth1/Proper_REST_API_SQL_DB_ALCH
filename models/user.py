## Import libraries
from common.database import Database
from db import db

## User Class
class UserModel(db.Model): ## Extend SQLAlchemy model for easier db interaction
    ## Setup SQLAchemy Variables
    ## Table
    __tablename__ = 'users'

    ## Table Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, _id: int, username: str, password: str) -> None:
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        """
        Find a given user in the database for authentication
        :param username: String input of the username
        :return: User object, user, we will use for auth
        """
        ## Setup Connection & Cursor
        connection, cursor = Database.connect_to_db()

        ## Find the user
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  ## Parameter must always be a tuple
        row = result.fetchone()  ## Returns None if no results

        ## Create User object if we get data back
        if row:
            user = cls(*row)
        else:
            user = None

        ## Close Connection
        Database.close_connection_to_db(connection)

        return user

    @classmethod
    def find_by_id(cls, _id):
        """
        Find a given user in the database for authentication
        :param _id: INT input fo the user_id
        :return: User object, user, we will use for auth
        """
        ## Setup Connection & Cursor
        connection, cursor = Database.connect_to_db()

        ## Find the user
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))  ## Parameter must always be a tuple
        row = result.fetchone()  ## Returns None if no results

        ## Create User object if we get data back
        if row:
            user = cls(*row)
        else:
            user = None

        ## Close Connection
        Database.close_connection_to_db(connection)

        return user