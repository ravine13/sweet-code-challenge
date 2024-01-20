from models import Vendor, Sweet, Vendor_Sweets
from app import app, db


def seed_data():

    vendors = [
        Vendor(name='Sweet Delights'),
        Vendor(name='Candy Corner'),
        Vendor(name='Sugar Rush'),
        Vendor(name='Tasty Treats'),
        Vendor(name='Delicious Delicacies'),
        Vendor(name='Confectionery Castle'),
        Vendor(name='Dessert Den'),
        Vendor(name='Pastry Palace'),
        Vendor(name='Bakery Bazaar'),
        Vendor(name='Treat Tower'),
    ]

    sweets = [
        Sweet(name='Chocolate Truffle'),
        Sweet(name='Vanilla Cupcake'),
        Sweet(name='Strawberry Tart'),
        Sweet(name='Blueberry Muffin'),
        Sweet(name='Raspberry Cheesecake'),
        Sweet(name='Lemon Loaf'),
        Sweet(name='Caramel Cookie'),
        Sweet(name='Pistachio Pastry'),
        Sweet(name='Almond Biscotti'),
        Sweet(name='Coconut Macaroon'),
    ]

   
    db.session.add_all(vendors)
    db.session.add_all(sweets)
    db.session.commit()

  
    vendor_sweets = []
    for i in range(10):
        price = f'{i+1}.99'
        sweet_id = sweets[i].id
        vendor_id = vendors[i].id
        vendor_sweet = Vendor_Sweets(price=price, sweets_id=sweet_id, vendor_id=vendor_id)
        vendor_sweets.append(vendor_sweet)

  
    db.session.add_all(vendor_sweets)
    db.session.commit()

    print("Seed data successfully updated.")

if __name__ == '__main__':
    with app.app_context():
        seed_data()
