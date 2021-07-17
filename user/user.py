from flask import jsonify, request
from flask_restful import Resource, abort
from flask_pymongo import pymongo
from bson.json_util import ObjectId
import db_config as database

class Patient(Resource):

	def get(self, by, data):
		response = self.abort_if_not_exist(by, data)
		response['_id'] = str(response['_id'])
		return jsonify(response)

	def post(self):
		_id = str(database.db.Patients.insert_one({
			'name': request.json['name'],
            'blood_pressure': request.json['blood_pressure'],
            'sugar_level': request.json['sugar_level'],
            'oxygen_level': request.json['oxygen_level'],
		}).inserted_id)

		return jsonify({"_id": _id})

	def put(self, by, data):
		response = self.abort_if_not_exist(by, data)

		for key, value in request.json.items():
			response[key] = value 

		database.db.Patients.update_one({'_id':ObjectId(response['_id'])},
		{'$set':{
			'name': response['name'],
            'blood_pressure': response['blood_pressure'],
            'sugar_level': response['sugar_level'],
            'oxygen_level': response['oxygen_level'],
		}}
		)

		response['_id'] = str(response['_id'])
		return jsonify(response)

	def delete(self, by, data):
		response = self.abort_if_not_exist(by, data)
		database.db.Patients.delete_one({'_id':response['_id']})
		response['_id'] = str(response['_id'])
		return jsonify({"deleted":response})

	def abort_if_not_exist(self, by, data):
		if by == "_id":
			response = database.db.Patients.find_one({"_id":ObjectId(data)})
		else:
			response = database.db.Patients.find_one({f"{by}": data})

		if response:
			return response
		else:
			abort(jsonify({"status":404, f"{by}":f"{data} not found"}))