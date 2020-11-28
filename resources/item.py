## Import libraries
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.item import ItemModel

## Item Class
class Item(Resource):
    ## Utilizing reqparse to only allow a price element - We do not want to update name
    parser = reqparse.RequestParser()  ## Use to parse the request

    ## Add specifics that parse will look for / enforce
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store id')

    @jwt_required  ## User must authenticate before calling method
    def get(self, name: str) -> tuple:  ## Currently allows items of same name
        """
        Take in the name and return the matching item
        :param name: Name of the item
        :return: Corresponding item or none if item not found
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    @jwt_required
    def post(self, name: str) -> tuple:
        """
        Search the db and insert if it does not exist
        :param name: Name of the item to search for / insert into the db
        :return: Item if successful, error message if not
        """
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name: str) -> tuple:
        """
        Delete an item from the database based on the item name
        :param name: Name of the item
        :return: Message that item was successfully deleted
        """
        ## Check is_admin
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege is required'}, 404

        ## Find the item
        item = ItemModel.find_by_name(name)

        if item:
            ## Delete from database
            item.delete_from_db()

        return {'message': 'Item deleted'}, 200

    @jwt_required
    def put(self, name: str) -> tuple:
        """
        Update if item already exists, insert if item does not exist
        :param name: Name of the item
        :return: Updated item or error message if unsuccessful
        """
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()
                
        return item.json(), 200

## ItemList Class
class ItemList(Resource):
    @jwt_required
    def get(self):
        """
        Return all items in the current items list
        :return: Items in the database
        """
        return {'items': [item.json() for item in ItemModel.find_all()]}
