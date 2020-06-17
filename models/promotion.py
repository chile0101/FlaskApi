from db import db
import json
from datetime import datetime

class PromotionModel(db.Model):
    __tablename__ = 'promotions'

    id = db.Column(db.Integer,primary_key=True)
    desc = db.Column(db.String(80))
    t1 = db.Column(db.String(30))
    t2 = db.Column(db.String(30))
    discount = db.Column(db.Integer)
    max_items = db.Column(db.Integer)
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product= db.relationship('ProductModel')


    def __init__(self, product_id, desc, t1, t2, discount, max_items):
        self.product_id = product_id
        self.desc = desc
        self.t1 = t1
        self.t2 = t2
        self.discount = discount
        self.max_items = max_items
    
    def json(self):
        return {'id': self.id,
                'desc': self.desc, 
                't1':self.t1,
                't2':self.t2,
                'discount': self.discount,
                'max_items': self.max_items,
                'product_id': self.product_id}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id) 
    
    def save_to_db(self):
        # print('self >>>>>>>>>>>>>>>>>>>', self.json())
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
