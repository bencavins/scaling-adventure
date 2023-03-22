from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'
    serialize_rules = ('-sweets.vendors', 'vendor_sweets.vendor')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    vendor_sweets = db.relationship('VendorSweet', backref='vendor')
    sweets = association_proxy('vendor_sweets', 'vendor', creator=lambda s: VendorSweet(sweet=s))

class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'
    serialize_rules = ('-vendors.sweets', '-vendor_sweets.sweet')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    vendor_sweets = db.relationship('VendorSweet', backref='sweet')
    vendors = association_proxy('vendor_sweets', 'sweet', creator=lambda v: VendorSweet(vendor=v))

class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'
    serialize_rules = ('-sweet.vendor_sweets', '-vendor.vendor_sweets')

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'))

    @validates('price')
    def validate_price(self, key, new_price):
        if new_price is None or new_price == '' or new_price < 0:
            raise ValueError(f'Invalid price: {new_price}')
        return new_price
