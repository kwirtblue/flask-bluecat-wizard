from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '24199e583c1f1de1bb8e499c0f1d5ff6625b040fde430747219c761f35e9c743'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wizard_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'Tmp/uploads'
app.config['ALLOWED_EXTENSIONS'] = ['.tgz', '.txt']
db = SQLAlchemy(app)

import routes

if __name__ == '__main__':
   app.run(debug=True)