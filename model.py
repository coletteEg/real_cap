from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(40), unique=True, nullable = False)
    password = db.Column(db.String, nullable=False)

    def get_id(self):
        return (self.user_id)

    def __init__ (self, email, password):
        self.email = email
        self.password = password
    def __repr__(self):
        return f'User email - {self.email}'

class Shark(db.Model):

    __tablename__ = 'sharks'

    shark_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    shark_name = db.Column(db.String, nullable = False)
    length = db.Column(db.Integer, nullable = False)
    weight = db.Column(db.Integer, nullable = False)
    diet = db.Column(db.String, nullable = False)
    image_url = db.Column(db.String, nullable = False)


    def __repr__(self):
        return (f"Shark: {self.shark_name}\n this shark is {self.length} feet long, weighs {self.weight} pounds and eats {self.diet}")


def connect_to_db(flask_app, db_uri="postgresql://WALL-E:sc@localhost:5432/buy_sharks", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///buy_sharks.db"
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")