## Import libraries
from db import db
from typing import Dict

## Item Class
class ItemModel(db.Model): ## Extend SQLAlchemy model for easier db interaction
    ## Setup SQLAchemy Variables
    ## Table
    __tablename__ = 'items'

    ## Table Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    ## Relate items and stores
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> Dict:
        return {'id': self.id,
                'name': self.name,
                'price': self.price,
                'store_id': self.store_id
        }

    @classmethod ## Keep as class because it returns an object of ItemModel
    def find_by_name(cls, name: str):
        """
        Search the items table for an existing item
        :param name: Name of the item
        :return: Item if exists in the db
        """
        return cls.query.filter_by(name=name).first() ## Use SQLAlchemy to build model from database data

    @classmethod
    def find_all(cls):
        return cls.query.all()

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