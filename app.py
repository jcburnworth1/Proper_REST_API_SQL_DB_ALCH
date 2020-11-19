## Reference Code - https://github.com/tecladocode/rest-api-sections/tree/master/section6
## Import libraries
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item, ItemList
from common.security import authenticate, identity

## Create the flask application
app = Flask(__name__)  # '__main__'
app.secret_key = 'lala'  ## If prod API, this would need to be a real key
api = Api(app)  ## Allow for easy resource addition with GET, POST, DELETE, etc.

## Return JWT token for auth later on
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)  # /auth

## Resources
api.add_resource(Item, '/item/<string:name>')  ## http://127.0.0.1:5000/item/chair
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

## Execute the program
if __name__ == '__main__':
    app.run(port=5000, debug=True)
