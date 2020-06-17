from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(4))
    color = db.Column(db.String(20))

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('ProductModel')

    def __init__(self, product_id, size, color):
        self.product_id = product_id
        self.size = size
        self.color = color

    def json(self):
        return {'id': self.id, 'size': self.size, 'color': self.color}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()