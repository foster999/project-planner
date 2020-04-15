from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)

sesion_object = Session(app)
db = SQLAlchemy(app)

from app import routes, models
