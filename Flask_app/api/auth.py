from xml.dom import UserDataHandler
from flask import Flask, request
from flask_restful import Resource, Api
import json
import datetime
import jwt

from .database import DB


class user(Resource):

    def get(self):

        try:
            username = request.args.get('username')
            password = request.args.get('password')

            if not username:
                return {'message': 'Username not specified.'}, 400
            
            if not password:
                return {'message': 'Password not specified.'}, 400


            if db.verify_user(username, password):

                token = jwt.encode({'username': username,
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                                    key=app.config['SECRET_KEY'],
                                    algorithm="HS256")

                return {'token': token}, 200

            return {'message': 'Invalid username or password.'}, 401

        except KeyError:
            return {'message': 'Invalid request format.'}, 400

        except DB.UserNotFound:
            return {'message': 'Invalid username or password.'}, 401

        except:
            return {'message': 'Unkown error.'}, 500


    def post(self):

        try:
            username = request.args.get('username')
            password = request.args.get('password')

            if not username:
                return {'message': 'Username not specified.'}, 400

            if not password:
                return {'message': 'Password not specified.'}, 400

            db.add_user(username, password)

            return {'message': 'User created successfully.'}, 201

        except DB.UserAlreadyExists:
            return {'message': 'User already exists.'}, 409

        except:
            return {'message': 'Unknown error.'}, 500



def init_auth(init_app: Flask, prefix: str, init_db: DB):

    global app, db
    app = init_app
    db = init_db

    api = Api(init_app)

    api.add_resource(user, prefix + "/user")



if __name__ == "__main__":

    new_app = Flask(__name__)
    new_app.secret_key = "top secret"

    new_db = DB()
    new_db.add_user('correct', 'correct')

    init_auth(new_app, '', new_db)

    new_app.run(debug=True)