from flask_login import UserMixin
from sqlalchemy import func

from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    books = db.relationship('Book', backref='user')
    transaction_categories = db.relationship('TransactionCategory', backref='user')
    item_categories = db.relationship('ItemCategory', backref='user')

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.String(100), nullable=True)

    transactions = db.relationship('Transaction', backref='book')


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    name = db.Column(db.String(100))
    location = db.Column(db.String(100), nullable=True)
    price = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    items = db.relationship('Item', backref='transaction')
    categories = db.relationship('TransactionCategory', secondary='category_transaction', backref='transactions')


class TransactionCategory(db.Model):
    __tablename__ = 'transaction_categories'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(100))
    emoji = db.Column(db.String(100))


category_transaction = db.Table(
    'category_transaction',
    db.Column('transaction_id', db.Integer, db.ForeignKey('transactions.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('transaction_categories.id'))
)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    name = db.Column(db.String(100))
    price = db.Column(db.String(100))
    categories = db.relationship('ItemCategory', secondary='category_item', backref='items')


class ItemCategory(db.Model):
    __tablename__ = 'item_categories'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(100))
    emoji = db.Column(db.String(100))


category_item = db.Table(
    'category_item',
    db.Column('item_id', db.Integer, db.ForeignKey('items.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('item_categories.id'))
)
