from flask_restful import Resource, reqparse
from models.promotion import PromotionModel
from models.product import ProductModel
from datetime import datetime

class Promotion(Resource):

    parser = reqparse.RequestParser()
    
    parser.add_argument('product_id', type=int, required=True, help="Every promotion item needs a product_id.")
    parser.add_argument('desc', type=str)
    parser.add_argument('t1', type=str, required=True, help="This field cannot be left blank !")
    parser.add_argument('t2', type=str, required=True, help="This field cannot be left blank !")
    parser.add_argument('discount', type=int, required=True, help="This field cannot be left blank !")
    parser.add_argument('max_items', type=int, required=True, help="This field can not be left blank !")


    def get(self):
        pass
    def post(self):

        data = Promotion.parser.parse_args()
        
        if ProductModel.find_by_id(data['product_id']) is None:
            return {'message':'Product not found.'},400
        
        t1 = datetime.strptime(data['t1'], "%d-%m-%Y %H:%M:%S")
        t2 = datetime.strptime(data['t2'], "%d-%m-%Y %H:%M:%S")

        if t1 > t2:
            return {'message': 'Start time must not be later than end time.'},400
        
        if data['discount'] > 100:
            return {'message': 'discount must not be bigger 100.'},400
        
        promotion_item = PromotionModel(data['product_id'],
                                        data['desc'],
                                        data['t1'],
                                        data['t2'],
                                        data['discount'],
                                        data['max_items'])
        
        try:
            promotion_item.save_to_db()
        except:
            return {"message": "An error occurred inserting the promotion item."}, 500

        return promotion_item.json(), 201

class PromotionList(Resource):

    def get(self):
        return {'promotions': list(map(lambda x: x.json(), PromotionModel.query.all()))}
