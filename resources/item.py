from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    
    parser.add_argument('product_id',
                        type=int,
                        required=True,
                        help="Every item needs a product_id.")

    def get(self, id):
        item = ItemModel.find_by_id(id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self):
    
        data = Item.parser.parse_args()

        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, id):
        item = ItemModel.find_by_id(id)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, id):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_id(id)

        if item:
            item.size = data['size']
            item.color = data['color']
            item.product_id = data['product_id']
        else:
            item = ItemModel(**data)

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}