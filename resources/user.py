## Import libraries
from flask_restful import Resource, reqparse
from models.user import UserModel

## UserRegister Class
class UserRegister(Resource):
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

        user = UserModel(**data) ## Unpack using * notation into user object
        user.save_to_db()

        return {"message": "User created successfully"}, 201
