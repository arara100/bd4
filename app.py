# app.py
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from routes import *


def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
