
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import db, Vendor, Sweet, Vendor_Sweets
import os
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db, render_as_batch=True)
db.init_app(app)
api = Api(app)
ma = Marshmallow(app)
ma.init_app(app)
CORS(app)

@app.route('/')
def home():
    return 'welcome to sunset sweets paradise'

class VendorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor

vendor_schema = VendorSchema()

class SweetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Sweet

sweet_schema = SweetSchema()

class Vendor_SweetsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor_Sweets
        fields = ("id", "price", "sweets_id", "vendor_id")

vendorSweet_schema = Vendor_SweetsSchema()

post_args = reqparse.RequestParser(bundle_errors=True)
post_args.add_argument('price', type=float, help='Price of the sweet', required=True)
post_args.add_argument('sweets_id', type=int, help='ID of the associated sweet', required=True)
post_args.add_argument('vendor_id', type=int, help='ID of the associated vendor', required=True)


class Vendors(Resource):
    def get(self):
        vendors = Vendor.query.all()
        res = vendor_schema.dump(vendors,many = True)

        response = make_response(
            jsonify(res),
            200
        )

        return response
api.add_resource(Vendors, '/vendors')

class VendorsByID(Resource):
    def get(self,id):
        vendor = Vendor.query.filter_by(id=id).first()

        if vendor is None:
            response = make_response(
                jsonify({"Error": "vendor not found"}),
                404
            )

            return response 
        else:
            sweets = Sweet.query.join(Vendor_Sweets).filter_by(vendor_id=id).all()
            sweets_res = [sweet_schema.dump(sweet) for sweet in sweets]
            vendor_res = vendor_schema.dump(vendor)
            vendor_res["sweets"] = sweets_res

            return vendor_res
        
api.add_resource(VendorsByID, '/vendor/<int:id>')

class Sweets(Resource):
    def get(self):
        sweets = Sweet.query.all()
        res = sweet_schema.dump(sweets,many = True)

        response = make_response(
            jsonify(res),
            200
        )
        return response
    
api.add_resource(Sweets, '/sweets')

class SweetByID(Resource):
    def get(self, id):
        sweet = Sweet.query.filter_by(id=id).first()

        if sweet is None:
            response = make_response(
                jsonify({"Error": "Sweet not found"}),
                404
            )
            return response
        else:
            response = make_response(
                jsonify(sweet_schema.dump(sweet)),
                200
            )
            return response

api.add_resource(SweetByID, '/sweet/<int:id>')


class vendor_sweet(Resource):
    def delete(self,id):
        vendor_sweets = Vendor_Sweets.query.get(id)

        if vendor_sweets:
            db.session.delete(vendor_sweets)
            db.session.commit()

            return {"message": "VendorSweet deleted successfully"}
        else:
            response = make_response(
                jsonify({"Error":"VendorSweet not found"}),
                404
            )

            return response
        
api.add_resource(vendor_sweet, '/vendor_sweets/<int:id>')


class new_VendorSweet(Resource):
    def post(self):
        data = post_args.parse_args()

        sweet = Sweet.query.get(data["sweets_id"])  
        vendor = Vendor.query.get(data["vendor_id"])

        if not (sweet and vendor):
            response = make_response(
                jsonify({"errors": ["Validation errors"]}),
                400
            )
            return response

        new_Vendor_sweet = Vendor_Sweets(**data)  

        db.session.add(new_Vendor_sweet)
        db.session.commit()

        sweet_data = sweet_schema.dump(sweet)  

        response = make_response(
            jsonify(sweet_data),
            201
        )
        return response

api.add_resource(new_VendorSweet, '/new_vendorsweets')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
