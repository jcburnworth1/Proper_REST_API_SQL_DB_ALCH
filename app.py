## Reference Code - https://github.com/tecladocode/rest-api-sections/tree/master/section6
## Import libraries
from common.db import db
from typing import Dict
from blacklist import BLACKLIST
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList


## Create the flask application
app = Flask(__name__)  # '__main__'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODFICATIONS'] = False ## Turn off flask sqlachemy tracking (not sqlachemy tracking)
app.config['PROPOGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
app.secret_key = 'lala'  ## If prod API, this would need to be a real key
api = Api(app)  ## Allow for easy resource addition with GET, POST, DELETE, etc.

@app.before_first_request
def create_tables():
    """
    Intiailize data.db automatically
    :return: none, data.db created in root
    """
    db.create_all()

## Return JWT token for auth later on
jwt = JWTManager(app) ## Does not create the auth endpoint like JWT

## Data we can attach to JWT payload
@jwt.user_claims_loader ## Modify function below and add to JWT manager / app
def add_claims_to_jwt(identity) -> Dict: ## Identity is the value of user.id we want to add claims to
    """
    Attach additional data we can user for things like token refresh
    :param identity: user.id
    :return: TF is user logging in is an admin
    """
    if identity == 1: ## Instead of hard-coding, you should read from a config or database
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['identity'] in BLACKLIST ## Contains value set when token created

@jwt.expired_token_loader
def expired_token_callback() -> tuple:
    """
    Notify user of invalid token error
    :return: Status message
    """
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error) -> tuple:
    """
    Notify user of invalid token error
    :param error: TBD
    :return: Status message
    """
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error) -> tuple:
    """
    Notify user of unauthorized token error
    :param error: TBD
    :return: Status message
    """
    return jsonify({
        'description': 'Request does not contain access token',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback() -> tuple:
    """
    Notify user of not fresh token error
    :return: Status message
    """
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback() -> tuple:
    """
    Notify user of revoked token error
    :return: Status message
    """
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401

## Resources
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Item, '/item/<string:name>')  ## http://127.0.0.1:5000/item/chair
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

## Execute the program
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
