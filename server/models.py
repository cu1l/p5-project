from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

# Models go here!

def same_as(column_name):
    def default_function(context):
        return context.current_parameters.get(column_name)
    return default_function

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-items", "-receipts")

    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, server_default=db.func.now())

    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    avatar = db.Column(db.String)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    rating = db.Column(db.Float)

    _password_hash = db.Column(db.String)

    items = db.relationship("Item", backref="user")
    receipts = db.relationship("Receipt", backref="user")

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        # utf-8 encoding and decoding is required in python 3
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

class Item(db.Model, SerializerMixin):
    __tablename__ = "items"

    serialize_rules = ("-receipts", "-carts")
    
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, server_default=db.func.now())

    name = db.Column(db.String)
    inventory = db.Column(db.Integer)
    price = db.Column(db.Float)
    image = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    receipts = db.relationship("Receipt", backref="items")

class Cart(db.Model, SerializerMixin):
    __tablename__ = "carts"

    serialize_rules = ("-reciepts", "-items")

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)

class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    reviewer_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)

class Receipt(db.Model, SerializerMixin):
    __tablename__ = "receipts"

    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True)
    
    item = db.Column(db.String)
    total = db.Column(db.Float)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))