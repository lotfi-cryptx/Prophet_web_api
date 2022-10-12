from flask import Flask, request
from flask_restful import Resource, Api
import jwt
import pandas as pd
from fbprophet import Prophet
import json
import io
import csv

from .database import DB, User


class models_list(Resource):

    def get(self):

        token = request.args.get('token')

        if not token:
            return {'message': 'Token not specified.'}, 401

        try:
            token_data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return {'message': 'Invalid token.'}, 401

        try:
            user = db.get_user(token_data['username'])

            models = []

            for model in user.models:
                models.append({'id': model.model_id, 'name': model.model_name, 'description': model.model_description})

            response = json.loads(json.dumps(models))

            return response, 200

        except DB.UserNotFound:
            return {'message': 'User not found.'}, 404

        #except Exception as e:
            #return {'message': f'Unknown error. error: {repr(e)}'}, 500



class model(Resource):

    def get(self):

        token = request.args.get('token')

        if not token:
            return {'message': 'Token not specified.'}, 401

        try:
            token_data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return {'message': 'Invalid token.'}, 401


        try:
            user = db.get_user(token_data['username'])

        except DB.UserNotFound:
            return {'message': 'User not found.'}, 404

        except:
            return {'message': 'Unknown error.'}, 500


        model_id_str = request.args.get('id')
        if not model_id_str:
            return {'message': 'Model id not specified'}, 400

        try:
            model_id = int(model_id_str)
        except:
            return {'message': 'model id must be an integer value.'}, 400


        forecast_period_str = request.args.get('forecast_period')
        if not forecast_period_str:
            return {'message': 'forecast_period not specified'}, 400

        try:
            forecast_period = int(forecast_period_str)
        except:
            return {'message': 'forecast_period must be an integer value.'}, 400


        try:
            m = user.get_model(model_id)

            future = m.model.make_future_dataframe(periods=forecast_period)

            forecast = m.model.predict(future)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

            dest = io.StringIO()
            writer = csv.writer(dest)

            forecast.to_csv()

            forecast_data = forecast.to_json(orient='values')

            response = {'model_id': model_id,
                        'model_name': m.model_name,
                        'data_columns': ['ds', 'yhat', 'yhat_lower', 'yhat_upper'],
                        'data_rows': json.loads(forecast_data)}

            return response, 200

        except User.ModelNotFound:
            return {'message': 'Model not found.'}, 404
        
        except:
            return {'message': 'Unknown error.'}, 500


    def post(self):

        token = request.args.get('token')

        if not token:
            return {'message': 'Token not specified.'}, 401

        try:
            token_data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return {'message': 'Invalid token.'}, 401

        try:
            user = db.get_user(token_data['username'])
        except DB.UserNotFound:
            return {'message': 'User not found.'}, 404


        model_name = request.form.get('model_name')
        model_description = request.form.get('model_description')
        model_data = request.files.get('model_data')

        if not model_name:
            return {'message': 'Invalid form data, model name not specified.'}, 400

        if not model_description:
            model_description = 'No Description.'

        if not model_data:
            return {'message': 'Invalid form data, model data file not specified.'}, 400

        try:
            df = pd.read_csv(model_data.stream)
        
            new_model = Prophet()
            new_model.fit(df)

            new_model_id = user.add_model(model_name, model_description, new_model)
        
            return {'id': new_model_id, 'model_name': model_name, 'model_description': model_description}, 200

        except:
            return {'message': 'Invalid csv data file format'}, 400



def init_prophet(init_app: Flask, prefix: str, init_db: DB):

    global app, db

    app = init_app
    db = init_db

    api = Api(init_app)

    api.add_resource(models_list, prefix + "/models")
    api.add_resource(model, prefix + "/model")



if __name__ == "__main__":

    test_app = Flask(__name__)
    test_app.config['SECRET_KEY'] = "top secret"

    test_db = DB()
    test_db.add_user('correct', 'correct')

    init_prophet(test_app, '', test_db)

    test_app.run(debug=True)