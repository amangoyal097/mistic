import zipfile
import os
from werkzeug.utils import secure_filename
import csv
from PIL import Image
import io
from base64 import encodebytes

ALLOWED_EXTENSIONS = set(['zip'])
UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__name__)), 'upload')
OUTPUT_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__name__)), 'output')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def unzip(file, folder):
    filename = secure_filename(file.filename)
    file.save(os.path.join(folder, filename))
    zip_ref = zipfile.ZipFile(os.path.join(folder, filename), 'r')
    file_names = zip_ref.namelist()
    zip_ref.extractall(folder)
    zip_ref.close()
    return file_names


def get_response_image(image_path):
    # reads the PIL image
    pil_img = Image.open(os.path.join(OUTPUT_FOLDER, image_path), mode='r')
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode(
        'ascii')  # encode as base64
    return encoded_img


def get_images():
    result = os.listdir(OUTPUT_FOLDER)
    encoded_images = []
    for image_path in result:
        encoded_images.append(get_response_image(image_path))
    return encoded_images
