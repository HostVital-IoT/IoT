from flask import Flask
from flask_restful import Api
from flask_cors import CORS

#Resources
from user.user import Patient
from user.users import Patients

app=Flask(__name__)
api=Api(app)
CORS(app)

api.add_resource(Patient, '/new/', '/<string:by>:<string:data>/')
api.add_resource(Patients, '/all')

if __name__ == '__main__':
  app.run(load_dotenv=True)