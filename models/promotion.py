from db import db
from datetime import datetime
from utils.utc_converter import utc_to_local
import json


class PromotionModel(db.Model):
    __tablename__ = 'promotions'

    id = db.Column(db.Integer,primary_key=True)
    desc = db.Column(db.String(80))
    t1 = db.Column(db.String(30))
    t2 = db.Column(db.String(30))
    discount = db.Column(db.Integer)
    max_items = db.Column(db.Integer)
    used_items = db.Column(db.Integer)
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product= db.relationship('ProductModel')


    def __init__(self, product_id, desc, t1, t2, discount, max_items):
        self.product_id = product_id
        self.desc = desc
        self.t1 = t1
        self.t2 = t2
        self.discount = discount
        self.max_items = max_items
        self.used_items = 0
    
    def json(self):
        return {'id': self.id,
                'desc': self.desc, 
                't1':self.t1,
                't2':self.t2,
                'discount': self.discount,
                'max_items': self.max_items,
                'used_items': self.used_items,
                'product_id': self.product_id}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id) 
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_promotion_items(cls, product_id):
        valid_items = []
        promotion_items = cls.query.filter_by(product_id = product_id).all()
        # print(promotion_items)
        for item in promotion_items:
            item_json = item.json()
            t1 = datetime.strptime(item_json['t1'], "%d-%m-%Y %H:%M:%S")
            t2 = datetime.strptime(item_json['t2'], "%d-%m-%Y %H:%M:%S")

            # print('nowwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',datetime.now())
            if t1 < utc_to_local(datetime.now()) < t2:
                if item_json['used_items'] < item_json['max_items']:
                    valid_items.append(item)
            
        return valid_items
