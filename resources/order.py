from flask_restful import Resource
from models.item import ItemModel
from models.product import ProductModel
from models.promotion import PromotionModel
from models.order import OrderModel


class Order(Resource):
    
    def get(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if item is None:
            return {
                'status': False,
                'message': 'Item not found',
                'data': None
            }

        product_id = item.json()['product_id']

        product = ProductModel.find_by_id(product_id)
        promotion_items = PromotionModel.find_promotion_items(product_id)

        sold_price = product.json()['price']
        
        if promotion_items:
            for p_item in promotion_items:
                sold_price -= (p_item.json()['discount']/100)*product.json()['price']
                p_item.used_items += 1
                p_item.save_to_db()
        
        order = OrderModel(item_id, float("{:.2f}".format(sold_price)))

        order.save_to_db()
        
        item.delete_from_db()

        return {
            'status': True,
            'message': 'A item has been sold.',
            'data': order.json()
        }
            
        
        
        