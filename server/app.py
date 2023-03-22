#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Vendor, Sweet, VendorSweet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/vendors')
def vendors():
    vendors = Vendor.query.all()
    data = [v.to_dict() for v in vendors]
    return make_response(jsonify(data), 200)

@app.route('/vendors/<int:id>')
def vendor_by_id(id):
    vendor = Vendor.query.filter(Vendor.id == id).first()

    if not vendor:
        return make_response(jsonify({
            'error': 'Vendor not found'
        }), 404)

    return make_response(jsonify(vendor.to_dict()), 200)

@app.route('/sweets')
def sweets():
    sweets = Sweet.query.all()
    data = [s.to_dict() for s in sweets]
    return make_response(jsonify(data), 200)

@app.route('/sweets/<int:id>', methods=['GET', 'PATCH'])
def sweet_by_id(id):
    sweet = Sweet.query.filter(Sweet.id == id).first()

    if not sweet:
        return make_response(jsonify({
            'error': 'Sweet not found'
        }), 404)

    if request.method == 'GET':
        return make_response(jsonify(sweet.to_dict()), 200)
    
    elif request.method == 'PATCH':
        data = request.get_json()
        for field, value in data.items():
            setattr(sweet, field, value)
        # for key in data:
        #     setattr(sweet, key, data[key])
        db.session.add(sweet)
        db.session.commit()
        return make_response(jsonify(sweet.to_dict()), 200)

@app.route('/vendor_sweets', methods=['POST'])
def vendor_sweets():
    data = request.get_json()
    try:
        vs = VendorSweet(
            price=data.get('price'),
            vendor_id=data.get('vendor_id'),
            sweet_id=data.get('sweet_id')
        )
    except ValueError as e:
        return make_response(jsonify({
            'error': [str(e)]
        }), 422)
    db.session.add(vs)
    db.session.commit()

    return make_response(jsonify(vs.to_dict()), 201)

@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def vendor_sweet_by_id(id):
    vs = VendorSweet.query.filter(VendorSweet.id == id).first()

    if not vs:
        return make_response(jsonify({
            'error': 'VendorSweet not found'
        }), 404)

    db.session.delete(vs)
    db.session.commit()
    return make_response(jsonify({}), 200)


if __name__ == '__main__':
    app.run(port=5555)
