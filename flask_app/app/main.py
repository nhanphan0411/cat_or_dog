from blueprints import home_page
from flask import Flask, Blueprint, render_template, request
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import re
import base64
import numpy as np 
import os
from werkzeug.utils import secure_filename
import sql 

app = Flask(__name__)
app.register_blueprint(home_page)
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/static/images/'

model = tf.keras.models.load_model('/Users/nhanpham/CoderSchool/week6/flask_app/app/models/nhan_catmodel.h5')

def parse_img(path):
    image = path
    image = load_img(image)
    image = img_to_array(image)
    image = tf.image.resize(image, [150,150])
    image /= 255.0
    image = np.expand_dims(image, 0)
    return image

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            f = request.files['file']
            if f:
                path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                f.save(path)
                image = parse_img(path)
                prediction = model.predict(image)
                if prediction[0][0] < 0.5:
                    prediction = 'cat'
                else:
                    prediction = 'dog'
                return render_template('predict.html', path = f.filename, predict = prediction)        
        except:
            data = request.json
            label = data.split()[0]
            img = data.split()[1]
            
            label = {'cat': 0, 'dog':1}.get(label)
            path = os.path.join(app.config['UPLOAD_FOLDER'], img)
            
            sql.create_table()
            sql.save_into_db(path, label)
            os.remove(path)
            return render_template('predict.html', path = "#", predict = "")


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 