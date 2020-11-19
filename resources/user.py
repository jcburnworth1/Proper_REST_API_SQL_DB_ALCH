## Import libraries
from flask_restful import Resource, reqparse
from common.database import Database
from models.user import UserModel

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

    def post(self) -> tuple:
        """
        Add a new user to the database if not exists
        :return: Message of successful add or error that user already exists
        """
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        connection, cursor = Database.connect_to_db()

        query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (data['username'], data['password']))

        ## Close Connection
        Database.close_connection_to_db(connection)

        return {"message": "User created successfully"}, 201
