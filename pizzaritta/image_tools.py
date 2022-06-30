import os  
from PIL import Image
from flask import current_app
from . import config


def generate_pictures(image_file, product_id):
    image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_file.filename))
    image_path = Image.open(config.PATH_TO_IMAGES+image_file.filename)
    str_product_id = str(product_id)
    sizes = [163, 333, 555]
    for size in sizes:
        new_image = image_path.resize((size, size))
        new_image.save(f"{config.PATH_TO_IMAGES}{size}/{str_product_id}.jpeg")
    os.remove(config.PATH_TO_IMAGES+image_file.filename)
