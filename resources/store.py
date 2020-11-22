## Import libraries
from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel
from typing import Dict

## Store Class
class Store(Resource):
    @jwt_required()
    def get(self, name) -> tuple:
        """

        :param name:
        :return:
        """
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name) -> tuple:
        """

        :param name:
        :return:
        """
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name) -> Dict:
        """

        :param name:
        :return:
        """
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}

## StoreList Class
class StoreList(Resource):
    @jwt_required()
    def get(self) -> Dict:
        """

        :return:
        """
        return {'stores': [store.json() for store in StoreModel.find_all()]}
