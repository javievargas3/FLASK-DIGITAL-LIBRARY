@api.route('/books', methods = ['POST'])
@token_required
def create_contact(current_user_token):
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

@api.route('/books', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    books = books.query.filter_by(user_token = a_user).all()
    response = book_schema.dump(books)
    return jsonify(response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_contact_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        book = book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    book = book.query.get(id) 
    book.author = request.json['author']
    book.email = request.json['title']
    book.phone_number = request.json['legnth']
    book.address = request.json['type']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = books_schema.dump(book)
    return jsonify(response)