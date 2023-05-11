#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Item, Cart, Receipt

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():

        print("Starting seed...")

        User.query.delete()
        Item.query.delete()
        Cart.query.delete()
        Receipt.query.delete()

        users = []
        for i in range(10):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                avatar=fake.image_url(),
                verified=fake.boolean(),
                rating=fake.pyfloat(min_value=0, max_value=5),
            )
            user.password_hash = fake.password()
            users.append(user)
        db.session.add_all(users)
        db.session.commit()

        items = []
        for i in range(25):
            item = Item(
                name=fake.word(),
                inventory=fake.random_int(min=0, max=100),
                price=fake.pyfloat(min_value=0, max_value=1000),
                image=fake.image_url(),
            )
            items.append(item)
        db.session.add_all(items)
        db.session.commit()