from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user

from . import db
from .models import Book, Transaction, TransactionCategory

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
    book = Book.query.filter_by(id=book_id).first()

    if int(book_id) not in list(map(lambda b: b.id, current_user.books)):
        abort(403)

    return render_template('transactions.html', book=book)


@main.route('/books/<book_id>/transactions')
@login_required
def add_transaction(book_id):
    if int(book_id) not in list(map(lambda b: b.id, current_user.books)):
        abort(403)
    return render_template('add_transaction.html', book_id=book_id)


@main.route('/books/<book_id>/transactions/add', methods=["POST"])
@login_required
def add_transaction_post(book_id):
    if int(book_id) not in list(map(lambda b: b.id, current_user.books)):
        abort(403)
    name = request.form['name']
    location = request.form['location']
    price = str(request.form['price'])

    new_transaction = Transaction(name=name, location=location, price=price, book_id=book_id)

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
    return render_template('categories/add_transaction.html')


@main.route('/categories/transaction', methods=["POST"])
@login_required
def add_transaction_category_post():
    title = request.form['title']

    new_category = TransactionCategory(title=title, user_id=current_user.id)

    db.session.add(new_category)
    db.session.commit()

    return redirect(url_for('main.show_categories'))

