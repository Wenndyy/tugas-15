from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Product('{self.nama}', {self.jumlah}, {self.harga})"
