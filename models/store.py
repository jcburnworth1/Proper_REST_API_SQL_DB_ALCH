## Import libraries
from db import db
from typing import Dict

## Store Class
class StoreModel(db.Model): ## Extend SQLAlchemy model for easier db interaction
    ## Setup SQLAchemy Variables
    ## Table
    __tablename__ = 'stores'

    ## Table Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    ## Pull back all items associated with given store
    items = db.relationship('ItemModel', lazy='dynamic') ## List of item models but don't load until StoreModel.json is called

    def __init__(self, name: str):
        self.name = name

    def json(self) -> Dict:
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod ## Keep as class because it returns an object of ItemModel
    def find_by_name(cls, name: str):
        """
        Search the items table for an existing item
        :param name: Name of the item
        :return: Item if exists in the db
        """
        return cls.query.filter_by(name=name).first() ## Use SQLAlchemy to build model from database data

    def save_to_db(self) -> None:
        """
        Upsert an item into the items table
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """
        Delete an item from the items table
        :return:
        """
        db.session.delete(self)
        db.session.commit()