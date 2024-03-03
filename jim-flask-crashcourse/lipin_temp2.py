from market import app, db
from market.models import Item, User

with app.app_context():
    for user in User.query.all():
        name = user.username
        print(f'name: {name}')