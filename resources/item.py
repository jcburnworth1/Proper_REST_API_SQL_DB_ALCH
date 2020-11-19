## Import libraries
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from common.database import Database
from models.item import ItemModel

##################### Example #####################
## All resources must be classes and inherit from Resource class
## Student Class / Resource
# class Student(Resource):
#     ## Resource that can only be access with a GET method
#     def get(self, name):
#         return {'student': name}

## Add student resource
# api.add_resource(Student, '/student/<string:name>') ## http://127.0.0.1:5000/student/JC
###################################################

## Item Class
class Item(Resource):

    ## Utilizing reqparse to only allow a price element - We do not want to update name
    parser = reqparse.RequestParser()  ## Use to parse the request
    ## Add specifics that parse will look for / enforce
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')

    @jwt_required()  ## User must authenticate before calling method
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

    def post(self, name: str) -> tuple:
        """
        Search the db and insert if it does not exist
        :param name: Name of the item to search for / insert into the db
        :return: Item if successful, error message if not
        """
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 200

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name: str) -> tuple:
        """
        Delete an item from the database based on the item name
        :param name: Name of the item
        :return: Message that item was successfully deleted
        """
        ## Setup Connection & Cursor
        connection, cursor = Database.connect_to_db()

        ## Delete the item from the database
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        ## Close Connection
        Database.close_connection_to_db(connection)

        return {'message': 'Item deleted'}, 200

    @jwt_required()
    def put(self, name: str) -> tuple:
        """
        Update if item already exists, insert if item does not exist
        :param name: Name of the item
        :return: Updated item or error message if unsuccessful
        """
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item."}, 500
                
        return updated_item.json(), 200

## ItemList Class
class ItemList(Resource):
    ## Table Name
    TABLE_NAME = 'items'

    @jwt_required()
    def get(self) -> tuple:
        """
        Return all items in the current items list
        :return: Items in the database
        """
        ## Setup Connection & Cursor
        connection, cursor = Database.connect_to_db()

        ## Retrieve all items
        ## Get the data
        query = "SELECT * FROM items"
        result = cursor.execute(query)

        ## Add all returned records to list
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        ## Close Connection
        Database.close_connection_to_db(connection)

        return items, 200