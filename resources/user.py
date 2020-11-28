## Import libraries
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel
from werkzeug.security import safe_str_cmp

## Setup parser object to look for username / password KV in JSON
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )

## UserRegister Class
class UserRegister(Resource):

    def post(self) -> tuple:
        """
        Add a new user to the database if not exists
        :return: JSON, HTML response
        """
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        user = UserModel(**data) ## Unpack using * notation into user object
        user.save_to_db()

        return {"message": "User created successfully"}, 201

## User Class
class User(Resource):
    @classmethod
    def get(cls, user_id) -> tuple:
        """
        Take a user_id and find a user model
        :param user_id:
        :return: JSON, HTML response
        """
        ## Parse the incoming JSON data
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'User not found'}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id) -> tuple:
        """
        Delete the record associated with a given user_id
        :param user_id:
        :return: JSON, HTML response
        """
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'User does not exists'}, 404

        user.delete_from_db()

        return {'message': 'User deleted'}, 200

## User Login
class UserLogin(Resource):

    @classmethod
    def post(cls) -> tuple:
        """
        Authenticate user into the API
        :return:
        """
        ## Parse the incoming JSON data
        data = _user_parser.parse_args()

        ## Find user in the database
        user = UserModel.find_by_username(data['username'])

        ## Check user password
        if user and safe_str_cmp(user.password, data['password']):
            ## Create token
            access_token = create_access_token(identity=user.id, fresh=True)

            ## Create refresh token
            refresh_token = create_refresh_token(identity=user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        ## If user doesn't exists
        return {'message': 'Invalid credentials'}, 401






