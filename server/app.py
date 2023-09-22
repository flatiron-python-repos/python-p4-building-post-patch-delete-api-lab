#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>', methods=["GET", "PATCH"])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if(request.method == "GET"):
        bakery_serialized = bakery.to_dict()

        response = make_response(
            bakery_serialized,
            200
        )
        return response
    else:
        bakery.name = request.form.get("name")

        db.session.commit()

        return jsonify({
            "id": bakery.id,
            "name": bakery.name
        }), 200


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    # data = request.get_json()
    new_baked_good = BakedGood(
        name = request.form.get('name'),
        price = request.form.get('price'),
        bakery_id = request.form.get('bakery_id')
    )

    db.session.add(new_baked_good)
    db.session.commit()

    return jsonify({
        "id": new_baked_good.id,
        "name": new_baked_good.name,
        "price": new_baked_good.price,
        "bakery_id": new_baked_good.bakery_id
    }), 201

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    # data = request.get_json()
    bake_to_delete = BakedGood.query.filter_by(id = id).first_or_404()

    db.session.delete(bake_to_delete)
    db.session.commit()

    return jsonify({
        "message": "User deleted successfully"
    }), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
