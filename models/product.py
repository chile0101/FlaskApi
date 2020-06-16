from db import db

class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    category = db.Column(db.String(80))
    vendor = db.Column(db.String(80))
    
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, price, category, vendor):
        self.name = name
        self.price = price
        self.category = category
        self.vendor = vendor
    
    def json(self):
        return {'id': self.id,
                'name': self.name, 
                'price':self.price,
                'category':self.category,
                'vendor': self.vendor,
                'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()