from flask_restful import Resource, reqparse
from models.item import ItemModel
from models.product import ProductModel


class Item(Resource):
    parser = reqparse.RequestParser()
    
    parser.add_argument('size', type=str)
    parser.add_argument('color', type=str)

    def get(self, id):
        item = ItemModel.find_by_id(id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, product_id):
    
        data = Item.parser.parse_args()

        item = ItemModel(product_id, **data)
        # print(item)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

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

    def put(self, product_id, item_id):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_id(item_id)
        product = ProductModel.find_by_id(product_id)
        
        if product:
            if item:
                if item.product_id != product_id:
                    return {'message': 'This item not in product'}, 400
                item.size = data['size']
                item.color = data['color']
                
            else:
                item = ItemModel(product_id,**data)
            
            item.save_to_db()
            return item.json()

        else:
            return {'message': 'Product not found'}, 404

class ItemList(Resource):
    def get(self, product_id):
        #print('>>>>>>>>>>>>',product_id)
        product = ProductModel.find_by_id(product_id)
        if product:
            return {'items': product.json()['items']}
        else:
           return {'message': 'Product not found'}, 404