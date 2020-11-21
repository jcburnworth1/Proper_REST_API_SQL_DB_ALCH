## Import libraries
from db import db

## User Class
class UserModel(db.Model): ## Extend SQLAlchemy model for easier db interaction
    ## Setup SQLAchemy Variables
    ## Table
    __tablename__ = 'users'

    ## Table Columns
    id = db.Column(db.Integer, primary_key=True) ## Auto incrementing
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        """
        Find a given user in the database for authentication
        :param username: String input of the username
        :return: User object, user, we will use for auth
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        """
        Find a given user in the database for authentication
        :param _id: INT input fo the user_id
        :return: User object, user, we will use for auth
        """
        return cls.query.filter_by(id=_id).first()