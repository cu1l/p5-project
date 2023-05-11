#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, jsonify, make_response, session
from flask_restful import Resource

# Local imports
from config import app, db, api
from models import User, Item, Receipt, Cart, Review

app.secret_key = b'\xfd\x94(\x8b\xda\xe1\xee\xdc5\xcb\x88\x0b&\xb4\xc7\xa3'

# Views go here!

class Login(Resource):
    def post(self):
        data = request.get_json()

        check_user = User.query.filter(User.username == data['username']).first()
        
        if check_user and check_user.authenticate(data['password']):
            session['user_id'] = check_user.id
            return make_response(check_user.to_dict(), 200)
        return {'error': 'Unauthorized'}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        return {'error': '401 Unauthorized'}, 401

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        avatar = data.get('avatar')

        new_user = User(
            username = username,
            avatar = avatar,
            first_name = first_name,
            last_name = last_name
        )

        new_user.password_hash = password

        try:
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return make_response(new_user.to_dict(), 201)

        except Exception as e:
            print(e)
            return make_response({'error': 'Unprocessable Entity'}, 417)
        
class Items(Resource):
    def get(self):
        all_items = []

        for item in Item.query.all():
            dict_item = item.to_dict()
            user_id = dict_item["user_id"]
            user_obj = User.query.filter_by(id=user_id).first()

            if user_obj:
                dict_item["user_rating"] = user_obj.to_dict()["rating"]

            all_items.append(dict_item)

        response = make_response(
            jsonify(all_items),
            200
        )

        return response
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        inventory = data.get('inventory')
        price = data.get('price')
        user_id = data.get('user_id')
        image = data.get('image')


        new_item = Item(
            name = name,
            inventory = inventory,
            price = price,
            user_id = user_id,
            image = image
        )

        try:
            db.session.add(new_item)
            db.session.commit()
            return make_response(new_item.to_dict(), 201)
        
        except Exception as e:
            print(e)
            return make_response({'error': 'Unprocessable Entity'}, 417)

class ItemByID(Resource):
    def get(self, id):
        item = Item.query.filter_by(id=id).first()
        if item:
            return make_response(item.to_dict())
        else:
            return make_response({"error": "Item not found"}, 404)
    
    def patch(self, id):
        item = Item.query.filter_by(id=id).first()
        if not item:
            return make_response({"error": "Item not found"}, 404)
        new_name = request.json.get('name')
        new_inventory = request.json.get('inventory')
        new_price = request.json.get('price')
        print(f"display name: {new_name}, ineventory: {new_inventory}, price: {new_price}")
        current_module_id = request.json.get('current_module_id')

        if new_name:
            item.name = new_name

        if new_inventory:
            item.inventory = new_inventory

        if new_price:
            item.price = new_price

        db.session.add(item)
        db.session.commit()
        return make_response(item.to_dict(), 200)
    
    def delete(self, id):
        item = Item.query.filter_by(id=id).first()
        if not item:
            return make_response({"error": "Item not found"}, 404)
        db.session.delete(item)
        db.session.commit()
        return make_response({}, 200)
    
class Carts(Resource):
    def get(self):
        all_carts = []
        cart_total = 0
        for cart in Cart.query.all():
            item_dict = cart.to_dict()
            item_id = item_dict["item_id"]
            item_obj_dict = Item.query.filter_by(id=item_id).first().to_dict()
            item_owner = item_obj_dict["user_id"]
            user_obj = User.query.filter_by(id=item_owner).first()
            if user_obj:
                item_obj_dict["item_owner_rating"] = user_obj.to_dict()["rating"]
            item_obj_dict["cart_owner_id"] = item_dict["user_id"]
            item_obj_dict["cart_entry_id"] = item_dict["id"]
            cart_total = cart_total + item_obj_dict["price"]
            all_carts.append(item_obj_dict)

        for item_dict in all_carts:
            item_dict["cart_total"] = cart_total
            
        return make_response(jsonify(all_carts), 200)
    
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        item_id = data.get('item_id')

        new_item = Cart(
            user_id = user_id,
            item_id = item_id
        )

        try:
            db.session.add(new_item)
            db.session.commit()
            return make_response(new_item.to_dict(), 201)
        
        except Exception as e:
            print(e)
            return make_response({'error': 'Unprocessable Entity'}, 417)

class CartById(Resource):
    def delete(self, id):
        cart = Cart.query.filter_by(id=id).first()
        if not cart:
            return make_response({"error": "Item not found"}, 404)
        db.session.delete(cart)
        db.session.commit()
        return make_response({}, 200)

class Receipts(Resource):
    def get(self):
        all_receipts = []

        for receipt in Receipt.query.all():
            dict_receipt = receipt.to_dict()
            all_receipts.append(dict_receipt)

        response = make_response(
            jsonify(all_receipts),
            200
        )
        return response
    
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        item_id = data.get('item_id')
        total = data.get('total')
        item_list = data.get('items')

        new_receipt = Receipt(
            user_id = user_id,
            item_id = item_id,
            total = total,
            item = item_list
        )

        try:
            db.session.add(new_receipt)
            db.session.commit()
            return make_response(new_receipt.to_dict(), 201)
        
        except Exception as e:
            print(e)
            return make_response({'error': 'Unprocessable Entity'}, 417)

class CheckSession(Resource):

    def get(self):
        user_id = session.get('user_id')
        
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        
        current_user = User.query.filter(User.id == user_id).first()
        return current_user.to_dict(), 200

class UserByID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(user.to_dict())
        else:
            return make_response({"error": "No User found"}, 404)
    
    def patch(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response({"error": "User not found"}, 404)
        new_username = request.json.get('username')
        new_avatar = request.json.get('avatar')
        new_email = request.json.get('email')
        new_verified = request.json.get('verified')
        print(f"username:{new_username}, avatar:{new_avatar}, email:{new_email}")
        current_module_id = request.json.get('current_module_id')
        new_rating = request.json.get('rating')

        # if current_module_id:
        #     user.current_module_id = current_module_id

        if new_username:
            user.username = new_username

        if new_avatar:
            user.avatar = new_avatar

        if new_rating:
            user.rating = new_rating

        if new_email:
            user.email = new_email

        if new_verified:
            user.verified = new_verified

        db.session.add(user)
        db.session.commit()
        return make_response(user.to_dict(), 200)
    
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response({"error": "User not found"}, 404)
        db.session.delete(user)
        db.session.commit()
        return make_response({}, 200)

class Reviews(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        reviewer_id = data.get('reviewer_id')
        rating = data.get('rating')
        
        new_review = Review(
            user_id = user_id,
            reviewer_id = reviewer_id,
            rating = rating
        )

        final_rating = rating
        rating_amount = 1
        user_obj = User.query.filter_by(id=user_id).first()
        if user_obj:
            user_obj_dict = user_obj.to_dict()
            reviews = Review.query.filter_by(user_id=user_id).all()
            if reviews:
                for review in reviews:
                    rev_dict = review.to_dict()
                    final_rating = final_rating + rev_dict["rating"]
                    rating_amount = rating_amount + 1

            final_rating = final_rating / rating_amount

            user_obj.rating = final_rating

            db.session.add(user_obj)
            db.session.commit()


        try:
            db.session.add(new_review)
            db.session.commit()
            return make_response(new_review.to_dict(), 201)
        
        except Exception as e:
            print(e)
            return make_response({'error': 'Unprocessable Entity'}, 417)

    

api.add_resource(Signup, '/signup')
api.add_resource(Reviews, '/review')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(UserByID, '/user/<int:id>')
api.add_resource(Items, '/items')
api.add_resource(ItemByID, '/items/<int:id>')
api.add_resource(Carts, '/carts')
api.add_resource(CartById, '/cart/<int:id>')
api.add_resource(Receipts, '/receipt')
api.add_resource(CheckSession, '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)