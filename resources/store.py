## Import libraries
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.store import StoreModel

## Store
class Store(Resource):
    @jwt_required
    def get(self, name) -> tuple:
        """
        Retrieve the store base on incoming name
        :param name: Name (integer id) of the store
        :return: Store json if found, message if not found
        """
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404

    @jwt_required
    def post(self, name) -> tuple:
        """
        Add a new store to the database
        :param name: Name (integer id) of the store
        :return: Store JSON if successful, message if not successful
        """
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    @jwt_required
    def delete(self, name) -> tuple:
        """
        Delete a store from the database
        :param name: Name (integer id) of the store
        :return: Message if successful or failure
        """
        ## Check is_admin
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege is required'}, 404

        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}, 200

## Store List
class StoreList(Resource):
    @jwt_required
    def get(self) -> tuple:
        """
        Return a list of all stores in the database
        :return: Store JSON
        """
        return {'stores': [store.json() for store in StoreModel.find_all()]}, 200
