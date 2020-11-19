## Import libraries
from flask_restful import Resource, reqparse
from common.database import Database

## User Class
class User:
    TABLE_NAME = 'users'

    def __init__(self, _id, username, password):
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
        query = "SELECT * FROM {table} WHERE username=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (username,))  ## Parameter must always be a tuple
        row = result.fetchone()  ## Returns None if no results

        ## Create User object if we get data back
        if row:
            user = cls(*row)
        else:
            user = None

        ## Close Connection
        connection.close()

        return user

    @classmethod
    def find_by_id(cls, _id):
        """
        Find a given user in the database for authentication
        :param id: INT input fo the user_id
        :return: User object, user, we will use for auth
        """
        ## Setup Connection & Cursor
        connection, cursor = Database.connect_to_db()

        ## Find the user
        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))  ## Parameter must always be a tuple
        row = result.fetchone()  ## Returns None if no results

        ## Create User object if we get data back
        if row:
            user = cls(*row)
        else:
            user = None

        ## Close Connection
        connection.close()

        return user

## UserRegister Class
class UserRegister(Resource):
    TABLE_NAME = 'users'

    ## Setup parser object to look for username / password KV in JSON
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        """
        Add a new user to the database if not exists
        :return: Message of successful add or error that user already exists
        """
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        connection, cursor = Database.connect_to_db()

        query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
