from market import app, db
from market.models import Item, User

# Create instances of Item for each row of sample data
phone = Item(name='Phone', price=500, barcode='893212299897', description='A high-quality smartphone')
laptop = Item(name='Laptop', price=900, barcode='123985473165', description='Powerful laptop for professional use')
keyboard = Item(name='Keyboard', price=150, barcode='231985128446', description='Ergonomic keyboard for comfortable use')
u1 = User(username='jsc', password_hash='123456', email_address='jsc@jsc.com')

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(u1)
    db.session.commit()
    # check to see if the data is in
    for user in User.query.all():
        name = user.username
        print(f'001 - User name: {name}')

    db.session.add(phone)
    db.session.add(laptop)
    db.session.add(keyboard)
    db.session.commit()
    for item in Item.query.all():
        name = item.name
        print(f'002 - Item name: {name}')

    for item in Item.query.filter_by(name='Phone'):
        price = item.price
        print(f'003 - phone price: {price}')

    # Assign a owner to item phone
    username = User.query.filter_by(username='jsc').first().username
    phone.owner = username
    db.session.add(phone)
    db.session.commit()

    print(f'004 - owner of phone: {phone.owner}')

# Add the instances to the session and commit to the database
# with app.app_context():
#     db.session.add(phone)
#     db.session.add(laptop)
#     db.session.add(keyboard)
#     db.session.commit()
#
# with app.app_context():
#     print('haha')
#     for item in Item.query.all():
#         name = item.name
#         price = item.price
#         description = item.description
#         barcode = item.barcode
#         print(f'{name} {price} {description} {barcode}')