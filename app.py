from flask import Flask
from flask import render_template
from flask import request
from main import main
from urllib.parse import quote
from urllib.request import urlopen
from flask_sqlalchemy import SQLAlchemy
from models import db,Developer
from flask_login import LoginManager
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'app-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(main)



if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)