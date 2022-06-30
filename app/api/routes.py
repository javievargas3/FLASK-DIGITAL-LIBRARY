from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}
#create book
@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    author = request.json['author']
    title = request.json['title']
    length = request.json['length']
    type = request.json['type']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book  = Book(author, title, length, type, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)
#read 
@api.route('/books', methods = ['GET'])
@token_required
def get_book(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = book_schema.dump(books)
    return jsonify(response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_book_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        book = Book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/books/<isbn>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,isbn):
    book = Book.query.get(isbn) 
    book.author = request.json['author']
    book.title = request.json['title']
    book.length = request.json['length']
    book.type = request.json['type']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('_books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = books_schema.dump(book)
    return jsonify(response)