import json

from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user

from . import db
from .models import Book, Transaction, TransactionCategory, Item, ItemCategory

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@main.route('/books')
@login_required
def books():
    return render_template('books.html', user=current_user)


@main.route('/books/add')
@login_required
def add_book():
    return render_template('add_book.html')


@main.route('/books', methods=["POST"])
@login_required
def add_book_post():
    name = request.form['name']
    description = request.form['description']

    new_book = Book(name=name, description=description, user_id=current_user.id)

    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for('main.books'))


@main.route('/books/<book_id>')
@login_required
def show_book(book_id):
    if int(book_id) not in list(map(lambda b: b.id, current_user.books)):
        abort(403)
    book = Book.query.filter_by(id=book_id).first()

    return render_template('transactions.html', book=book)


@main.route('/books/<book_id>/transactions')
@login_required
def add_transaction(book_id):
    if int(book_id) not in list(map(lambda b: b.id, current_user.books)):
        abort(403)
    book = Book.query.filter_by(id=book_id).first()
    return render_template('add_transaction.html', book=book)


@main.route('/books/<book_id>/transactions/add', methods=["POST"])
@login_required
def add_transaction_post(book_id):
    if int(book_id) not in list(map(lambda b: b.id, current_user.books)):
        abort(403)
    name = request.form['name']
    location = request.form['location']
    new_transaction = Transaction(name=name, location=location, price=0, book_id=book_id)

    items = json.loads(request.form['items'])
    for item in items:
        new_item = Item(name=item["name"], price=item["price"])
        categories = map(lambda c: ItemCategory.query.filter_by(id=c).first(), item['categories'])
        for c in categories: new_item.categories.append(c)

        new_transaction.items.append(new_item)
        new_transaction.price += int(item["price"])

    categories = map(lambda c: TransactionCategory.query.filter_by(id=c).first(), request.form.getlist('categories'))
    for c in categories: new_transaction.categories.append(c)

    db.session.add_all(new_transaction.items)
    db.session.add(new_transaction)
    db.session.commit()

    return redirect(url_for('main.show_book', book_id=book_id))


@main.route('/categories')
@login_required
def show_categories():
    return render_template('categories/show.html')


@main.route('/categories/transaction')
@login_required
def add_transaction_category():
    return render_template('categories/add_transaction_category.html')


@main.route('/categories/transaction', methods=["POST"])
@login_required
def add_transaction_category_post():
    title = request.form['title']
    emoji = request.form['emoji']

    new_category = TransactionCategory(title=title, user_id=current_user.id, emoji=emoji)

    db.session.add(new_category)
    db.session.commit()

    return redirect(url_for('main.show_categories'))


@main.route('/categories/item')
@login_required
def add_item_category():
    return render_template('categories/add_item_category.html')


@main.route('/categories/item', methods=["POST"])
@login_required
def add_item_category_post():
    title = request.form['title']
    emoji = request.form['emoji']

    new_category = ItemCategory(title=title, user_id=current_user.id, emoji=emoji)

    db.session.add(new_category)
    db.session.commit()

    return redirect(url_for('main.show_categories'))


@main.route('/books/<book_id>/transactions/<transaction_id>')
@login_required
def show_items(book_id, transaction_id):
    if int(book_id) not in list(map(lambda b: b.id, current_user.books)):
        abort(403)

    book = Book.query.filter_by(id=book_id).first()
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    return render_template('items.html', book=book, transaction=transaction)


@main.route('/books/<book_id>/transactions/<transaction_id>/add')
@login_required
def add_item(book_id, transaction_id):
    if int(book_id) not in list(map(lambda b: b.id, current_user.books)):
        abort(403)

    book = Book.query.filter_by(id=book_id).first()
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    return render_template('add_item.html', book=book, transaction=transaction)


@main.route('/books/<book_id>/transactions/<transaction_id>/add', methods=["POST"])
@login_required
def add_item_post(book_id, transaction_id):
    if int(book_id) not in list(map(lambda b: b.id, current_user.books)):
        abort(403)

    name = request.form['name']
    price = request.form['price']
    new_transaction = Transaction.query.filter_by(id=transaction_id).first()

    new_transaction.price = str(int(new_transaction.price) + int(price))

    new_item = Item(name=name, price=price)
    categories = map(lambda c: ItemCategory.query.filter_by(id=c).first(), request.form.getlist('categories'))
    for c in categories: new_item.categories.append(c)
    new_transaction.items.append(new_item)

    db.session.add(new_item)
    db.session.add(new_transaction)
    db.session.commit()

    return redirect(url_for('main.show_book', book_id=book_id))
