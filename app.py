## Reference Code - https://github.com/tecladocode/rest-api-sections/tree/master/section6
## Import libraries
from common.db import db
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

## Create the flask application
app = Flask(__name__)  # '__main__'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODFICATIONS'] = False ## Turn off flask sqlachemy tracking (not sqlachemy tracking)
app.config['PROPOGATE_EXCEPTIONS'] = True
app.secret_key = 'lala'  ## If prod API, this would need to be a real key
api = Api(app)  ## Allow for easy resource addition with GET, POST, DELETE, etc.

@app.before_first_request
def create_tables():
    db.create_all()

## Return JWT token for auth later on
jwt = JWTManager(app) ## Does not create the auth endpoint like JWT

## Resources
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Item, '/item/<string:name>')  ## http://127.0.0.1:5000/item/chair
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

## Execute the program
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
