from flask import Flask, flash, request, redirect, url_for
## both following dead ends
##from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
## from flask_uploads import UploadSet, configure_uploads

from flask_sqlalchemy import SQLAlchemy
import mariadb

import os

from werkzeug.utils import secure_filename

from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

## while testing without https
##>> os.environ["OAUTHLIB_INSECURE_TRANSPORT"]="1"

#UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,  instance_relative_config=True)
    #mail_server = environ.get('MAIL_SERVER')

    db.init_app(app)
    app.config.from_object('config')
    #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    from hello.routes import hello_page_bp
    from upload.routes import upload_page_bp
    app.register_blueprint(hello_page_bp)
    app.register_blueprint(upload_page_bp)
    return app