# Example of the use of Flask with HTML forms
# https://www.tutorialspoint.com/flask/flask_sending_form_data_to_template.htm

# Note: List existing flask jobs with: $ ps -fA | grep python
#       Kill current job with: kill -9 , <job_id>
# See: https://medium.com/@WhoIsShailesh/the-python-flask-problem-socket-error-errno-48-address-already-in-use-4d074847587e 

import numpy as np
import pandas as pd

import tensorflow as tf
print('Running on Tensorflow '+tf.__version__)  # Must be Tensorflow 2.x
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from tensorflow.keras.models import load_model

from flask import Flask, render_template, request
app = Flask(__name__)

print('Loading NN model...')
erie_model = load_model('erie_model_45005.h5')
erie_model.summary() 

@app.route('/')
def wind_inpput():
   return render_template('input.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form

      wspd = np.array([float(result['wspd_0h']), float(result['wspd_0h']), float(result['wspd_0h']), float(result['wspd_0h']), 
                      float(result['wspd_12h']), float(result['wspd_12h']), float(result['wspd_12h']), float(result['wspd_12h']), float(result['wspd_24h'])])
      wdir = np.array([float(result['wdir_0h']), float(result['wdir_0h']), float(result['wdir_0h']), float(result['wdir_0h']), 
                      float(result['wdir_12h']), float(result['wdir_12h']), float(result['wdir_12h']), float(result['wdir_12h']), float(result['wdir_24h'])])

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
      result = {'Station 45005': "{:.3f}".format(prediction[0,0]), 
                'Station 45142': "{:.3f}".format(prediction[0,1])}
      print(result)

      return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(debug = True)