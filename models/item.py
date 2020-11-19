## Import libraries
from common.database import Database
from typing import Dict

## Item Class
class ItemModel:
    ## Table Name
    TABLE_NAME = 'items'

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def json(self) -> Dict:
        return {'name': self.name, 'price': self.price}

    @classmethod ## Keep as class because it returns an object of ItemModel
    def find_by_name(cls, name: str):
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

        ## Close Connection
        Database.close_connection_to_db(connection)

        if row:
            return cls(*row) ## Argument unpacking example

    def insert(self) -> None:
        """
        Insert an item into the items table
        :param item: JSON object containing the item information
        :return: None
        """
        ## Setup Connection & Cursor
        connection, cursor = Database.connect_to_db()

        ## Insert the data
        query = "INSERT INTO {table} VALUES(?, ?)".format(table=ItemModel.TABLE_NAME)
        cursor.execute(query, (self.name, self.price))

        ## Close Connection
        Database.close_connection_to_db(connection)

    def update(self) -> None:
        """
        Update an item in the database
        :param item: Item to be updated
        :return: None
        """
        ## Setup Connection & Cursor
        connection, cursor = Database.connect_to_db()

        query = "UPDATE {table} SET price=? WHERE name=?".format(table=ItemModel.TABLE_NAME)
        cursor.execute(query, (self.price, self.name))

        ## Close Connection
        Database.close_connection_to_db(connection)
