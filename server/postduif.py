from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
db = SQLAlchemy(app)

class Duif():
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    speed = db.Column(db.Integer)
    level = db.Column(db.Integer)
    state = db.Column(db.Enum)
    home_loc = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, speed, level, state, home_loc, user_id):
        self.name = name
        self.speed = speed
        self.level = level
        self.state = state
        self.home_loc = home_loc
        self.user_id = user_id
