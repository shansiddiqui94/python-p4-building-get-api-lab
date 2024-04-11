#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakes = [bakery.to_dict() for bakery in Bakery.query.all()] 
    
    response = make_response(
        bakes,
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakes = Bakery.query.filter(Bakery.id == id).first()
    bake_dict = bakes.to_dict()
    response = make_response(
        bake_dict, 
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    #first query and sort of price
    baked_goods_desc = BakedGood.query.order_by(BakedGood.price.desc()).all()
    # convert the sorted list to a dict
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods_desc]
    #Finally create a response and status code
    response = make_response(
        baked_goods_list,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    most_expensive_dict = most_expensive_baked_good.to_dict() if most_expensive_baked_good else {}
    response = make_response(
        most_expensive_dict,
        200
    )
    return response 

if __name__ == '__main__':
    app.run(port=5555, debug=True)
