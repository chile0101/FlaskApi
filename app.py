from flask import Flask
from flask_restful import Api

from resources.item import Item, ItemList
from resources.product import Product, ProductList
from resources.promotion import Promotion, PromotionList
from resources.order import Order

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)


base_path = "/api"
api.add_resource(ProductList, base_path + '/products')
api.add_resource(Product, base_path +'/product', base_path + '/product/<int:id>')

api.add_resource(ItemList, base_path + '/product/<int:product_id>/items')
api.add_resource(Item, base_path + '/product/<int:product_id>/item', base_path + '/product/<int:product_id>/item/<int:item_id>') 

api.add_resource(PromotionList, base_path + '/promotions')
api.add_resource(Promotion, base_path + '/promotion')

api.add_resource(Order, base_path + '/sell/<int:item_id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)