from db import db
from datetime import datetime

class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.String(30))
    sold_price = db.Column(db.Float(precision=2))

    item_id = db.Column(db.Integer)
    

    def __init__(self, item_id, sold_price):
        self.item_id = item_id
        self.sold_price = sold_price
        self.create_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def json(self):
        return {'id': self.id, 'item_id': self.item_id, 'sold_price': self.sold_price,'create_at':self.create_at}

    # @classmethod
    # def find_by_id(cls, id):
    #     return cls.query.get(id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # def delete_from_db(self):
    #     db.session.delete(self)
    #     db.session.commit()