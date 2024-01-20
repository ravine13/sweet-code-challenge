from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, validates
from random import choices, randint
from datetime import datetime


db = SQLAlchemy()

class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow)
    sweets = db.relationship('Vendor_Sweets', back_populates='vendor')  

    def __repr__(self):
        return f'<vendor {self.name}>'


class Vendor_Sweets(db.Model):  
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.String(255), nullable=False)
    sweets_id = db.Column(db.Integer, db.ForeignKey('sweets.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow)
    sweet = db.relationship('Sweet', back_populates='vendor')  
    vendor = db.relationship('Vendor', back_populates='sweets')

    @validates('price')
    def validates_price(self, key, price):
        if not price:
            raise ValueError("Price cannot be blank")
        
        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be a negative number")

        return price

class Sweet(db.Model): 
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now(), onupdate=datetime.utcnow)
    vendor = db.relationship('Vendor_Sweets', back_populates='sweet')

