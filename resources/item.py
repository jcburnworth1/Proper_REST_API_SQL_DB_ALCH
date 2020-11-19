## Import libraries
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from common.database import Database

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
    ## Table Name
    TABLE_NAME = 'items'

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
        item = self.find_by_name(name)
        if item:
            return item, 200
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name: str) -> tuple:
        """
        Search the items table for an existing item
        :param name: Name of the item
        :return: Item if exists in the db
        """
        ## Setup Connection & Cursor
        connection, cursor = Database.connect_to_db()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200

    def post(self, name: str) -> tuple:
        """
        Search the db and insert if it does not exist
        :param name: Name of the item to search for / insert into the db
        :return: Item if successful, error message if not
        """
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 200

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            Item.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item, 201

    @classmethod
    def insert(cls, item: dict) -> None:
        """
        Insert an item into the items table
        :param item: JSON object containing the item information
        :return: None
        """
        ## Setup Connection & Cursor
        connection, cursor = Database.connect_to_db()

        ## Insert the data
        query = "INSERT INTO {table} VALUES(?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['name'], item['price']))

        ## Commit changes & close connection
        connection.commit()
        connection.close()

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
        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        ## Commit changes & close connection
        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}, 200

    @jwt_required()
    def put(self, name: str) -> tuple:
        """
        Update if item already exists, insert if item does not exist
        :param name: Name of the item
        :return: Updated item or error message if unsuccessful
        """
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item, 200

    @classmethod
    def update(cls, item: dict) -> None:
        """
        Update an item in the database
        :param item: Item to be updated
        :return: None
        """
        ## Setup Connection & Cursor
        connection, cursor = Database.connect_to_db()

        query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['price'], item['name']))

        ## Commit changes & close connection
        connection.commit()
        connection.close()

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
        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)

        ## Add all returned records to list
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        ## Close Connection
        connection.close()

        return items, 200
