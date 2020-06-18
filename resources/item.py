from flask_restful import Resource, reqparse
from models.item import ItemModel
from models.product import ProductModel


class Item(Resource):
    parser = reqparse.RequestParser()
    
    parser.add_argument('size', type=str)
    parser.add_argument('color', type=str)

    def post(self, product_id):
    
        data = Item.parser.parse_args()

        if ProductModel.find_by_id(product_id) is None:
            return {
                'status':False,
                'message': 'Product not found',
                'data': None
            }

        item = ItemModel(product_id, **data)
      
        item.save_to_db()

        return {
            'status':True,
            'message': 'A new item added to the product',
            'data': item.json()
        }

    def delete(self, product_id, item_id):
        item = ItemModel.find_by_id(item_id)
        product = ProductModel.find_by_id(product_id)
        
        if product:
            if item:
                if item.product_id != product_id:
                    return {'message': 'This item not in product'}, 400
                item.delete_from_db()
                return {'message':'Item deleted'}
            else:
                return {'message':'Item not found'}, 404
        else:
            return {'message': 'Product not found'}, 404


class ItemList(Resource):
    def get(self, product_id):
        
        product = ProductModel.find_by_id(product_id)
        if product:
            return {
                'status': True,
                'message': 'Success',
                'data': product.json()['items']}
        else:
            return {
                'status':False,
                'message': 'Product not found',
                'data': None
            }