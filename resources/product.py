from flask_restful import Resource, reqparse
from models.product import ProductModel

class Product(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('category',type=str)
    parser.add_argument('vendor',type=str)

    def get(self, id):
        product = ProductModel.find_by_id(id)
        if product:
            return product.json()
        return {'message': 'Product not found.'}, 404

    def post(self):
        
        product = Product.parser.parse_args()

        # print(product['name'])

        if ProductModel.find_by_name(product['name']):
            return {'message':"A product with name '{}' already exists.".format(product['name'])}
        
        product = ProductModel(**product)
    
        try:
            product.save_to_db()
        except:
            return {'message': 'An error occurred while creating the product.'}, 500
        
        return product.json(), 201
    
    def put(self,id):
        data = Product.parser.parse_args()

        product = ProductModel.find_by_id(id)

        if product:
            product.name = data['name']
            product.category = data['category']
            product.vendor = data['vendor']
        else:
            product = ProductModel(**data)

        product.save_to_db()

        return product.json()

    def delete(self, id):
        product = ProductModel.find_by_id(id)
        if product:
            product.delete_from_db()
        return {'message': 'Product deleted.'}
        

class ProductList(Resource):

    def get(self):
        return {'products': list(map(lambda x: x.json(), ProductModel.query.all()))}