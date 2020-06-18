from flask_restful import Resource, reqparse
from models.product import ProductModel
from models.promotion import PromotionModel

class Product(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('name', 
                        required=True, 
                        nullable=False, 
                        type=str, 
                        help="This field cannot be left blank!")
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('category',type=str)
    parser.add_argument('vendor',type=str)

    def get(self, id):

        product = ProductModel.find_by_id(id)
        promotion_items = PromotionModel.find_promotion_items(id)
        
        if product:
            product_json = product.json()
            if promotion_items:
                origin_price = product_json['price']
                sale_price = origin_price
                for item in promotion_items:
                    sale_price -= (item.json()['discount']/100)*origin_price
                product_json['sale_price'] = float("{:.2f}".format(sale_price))
            return {
                'status': True,
                'message': 'Success',
                'data': product_json
            }
            
        return {
            'status': False,
            'message': 'Product not found.',
            'data': None
        }, 404

    def post(self):
        
        product = Product.parser.parse_args()

        if not product['name']:
            return {
                'status': False,
                'message': 'Product name must not be empty.',
                'data': None
            }

        if ProductModel.find_by_name(product['name']):
            return {
                'status': False,
                'message':"A product with name '{}' already exists.".format(product['name']),
                'data': None
            }
        
        product = ProductModel(**product)
    
        try:
            product.save_to_db()
        except:
            return {
                'status': False,
                'message': 'An error occurred while creating the product.',
                'data': None
            }, 500
        
        return {
            'status': True,
            'message': 'Success',
            'data': product.json()
        },201

    
    def put(self,id):
        data = Product.parser.parse_args()

        product = ProductModel.find_by_id(id)

        if product is None:
            return {
                'status': False,
                'message':'Product not found',
                'data': None
            }

        if not data['name']:
            return {
                'status': False,
                'message': 'Product name must not be empty.',
                'data': None
            }

        if data['name'] != product.name:
            if ProductModel.find_by_name(data['name']):
                return {
                    'status': False,
                    'message': 'Product name is already exists.',
                    'data': None
                }

        product.name = data['name']
        product.price = data['price']
        product.category = data['category']
        product.vendor = data['vendor']
        
        product.save_to_db()

        return {
            'status': True,
            'message': 'The product has been updated.',
            'data': product.json()
        }

    def delete(self, id):
        product = ProductModel.find_by_id(id)

        if product is None:
            return {
                'status': False,
                'message': 'Product not found',
                'data': None
            }
        product.delete_from_db()
        return {
            'status': True,
            'message': 'Product has been deleted',
            'data': None
        }
        

class ProductList(Resource):

    def get(self):
        return {
            'status': True,
            'message': 'Success',
            'data': list(map(lambda x: x.json(), ProductModel.query.all()))
        }