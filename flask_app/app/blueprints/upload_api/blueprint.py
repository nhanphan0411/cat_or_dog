from flask import Blueprint, render_template, request
import tensorflow as tf
import re
import base64
import numpy as np 
import os
from werkzeug.utils import secure_filename


def parse_image(imgData):
    img_str = re.search(b"base64,(.*)", imgData).group(1)
    img_decode = base64.decodebytes(img_str)
    with open('output.png', "wb") as f:
        f.write(img_decode)
    return img_decode

model = tf.keras.models.load_model('models/nhan_catmodel.h5')

upload_api = Blueprint('upload_api', __name__)

