from flask import Flask
from flask_restful import Api

from resources.item import Item, ItemList
from resources.product import Product, ProductList
from resources.promotion import Promotion

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(ProductList, '/products')
api.add_resource(Product,'/product', '/product/<int:id>')

api.add_resource(ItemList, '/product/<int:product_id>/items')
api.add_resource(Item, '/product/<int:product_id>/item', '/product/<int:product_id>/item/<int:item_id>') 


api.add_resource(Promotion,'/promotion')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)