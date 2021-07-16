from flask import jsonify
from flask_restful import Resource

import db_config as database

class Patients(Resource):
    """ Get all the patients """
    def get(self):
        response = list(database.db.Patients.find())
        for doc in response:
            doc['_id'] = str(doc['_id'])
    
        return jsonify(response)