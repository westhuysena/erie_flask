# Example of the use of Flask with HTML forms
# https://www.tutorialspoint.com/flask/flask_sending_form_data_to_template.htm

import numpy as np
import pandas as pd

import tensorflow as tf
print('Running on Tensorflow '+tf.__version__)  # Must be Tensorflow 2.x
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from tensorflow.keras.models import load_model

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

print('Loading NN model...')
erie_model = load_model('erie_model_45005.h5')
erie_model.summary() 

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')

class PredictHs(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args['query']
        print(user_query)

        wspd_0h = user_query
        wdir_0h = 225
        print(wspd_0h, wdir_0h)
        wspd_12h = wspd_0h
        wspd_24h = wspd_0h
        wdir_12h = wdir_0h
        wdir_24h = wdir_0h

        wspd = np.array([float(wspd_0h), float(wspd_0h), float(wspd_0h), float(wspd_0h), 
                        float(wspd_12h), float(wspd_12h), float(wspd_12h), float(wspd_12h), float(wspd_24h)])
        wdir = np.array([float(wdir_0h), float(wdir_0h), float(wdir_0h), float(wdir_0h), 
                        float(wdir_12h), float(wdir_12h), float(wdir_12h), float(wdir_12h), float(wdir_24h)])

        print(wspd)
        print(wdir)

        wavdat12 = pd.DataFrame({'wspd1': wspd, 'wdir1': wdir, 'wspd2': wspd, 'wdir2': wdir})
        print(wavdat12.head(9))

        # Convert wind vectors to components
        UWND1 = wavdat12['wspd1']*np.cos((270. - wavdat12['wdir1'])*np.pi/180.)
        VWND1 = wavdat12['wspd1']*np.sin((270. - wavdat12['wdir1'])*np.pi/180.)
        UWND2 = wavdat12['wspd2']*np.cos((270. - wavdat12['wdir2'])*np.pi/180.)
        VWND2 = wavdat12['wspd2']*np.sin((270. - wavdat12['wdir2'])*np.pi/180.)

        test_data = pd.DataFrame({'UWND1': UWND1, 'VWND1': VWND1, 'UWND2': UWND2, 'VWND2': VWND2})
        print(test_data.head(9))
        test_data = np.reshape(test_data.to_numpy(), (1, 9, 4), order='C')
        print(test_data.shape)

        prediction = erie_model.predict(test_data)
        print(prediction)

        # create JSON object
        result = {'Station 45005': "{:.3f}".format(prediction[0,0]), 
                  'Station 45142': "{:.3f}".format(prediction[0,1])}
        print(result)
        
        return result

# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictHs, '/')

if __name__ == '__main__':
   app.run(debug = True)