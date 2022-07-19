from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from . import db
from .models import Book

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


@main.route('/add_book')
@login_required
def add_book():
    return render_template('add_book.html')


@main.route('/add_book', methods=["POST"])
@login_required
def add_book_post():
    name = request.form['name']

    new_book = Book(name=name, user_id=current_user.id)

    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for('main.books'))
