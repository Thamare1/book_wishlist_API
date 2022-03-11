from flask import Flask, jsonify, json, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column


# INSTANTIATE APP
app = Flask(__name__)

# DETERMINE THE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INSTANTIATE THE DATABASE MODEL
db = SQLAlchemy(app)


# CREATE THE SQLALCHEMY MODEL
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookTitle = db.Column(db.String(40))
    genre = db.Column(db.String(40))
    author = db.Column(db.String(40))
    ratings = db.Column(db.Integer)
    isTopSeller = db.Column(db.Boolean, default=False, server_default="false")
    # db.Boolean, default=False, nullable=False

    def __init__(self, BookTitle, genre, author, ratings, isTopSeller):
        self.bookTitle = BookTitle
        self.genre = genre
        self.author = author
        self.ratings = ratings
        self.isTopSeller = isTopSeller


# GET ALL PRODUCTS
@app.route('/books', methods=['GET'])
def get_books():
    # With sqlalchemy we don't need sql queries, we use the following format instead
    books = Book.query.all()
    bookArr = []
    for book in books:
        all_books = {
            "id": book.id,
            "bookTitle": book.bookTitle,
            "genre": book.genre,
            "author": book.author,
            "ratings": book.ratings,
            "isTopSeller": book.isTopSeller
        }
        bookArr.append(all_books)
    result = json.dumps(bookArr)
    return result


# CREATE A BOOK
@app.route('/book', methods=['POST'])
def insert_book():
    # Received posted data and store it in variables
    bookTitle = request.json['bookTitle']
    genre = request.json['genre']
    author = request.json['author']
    ratings = request.json['ratings']
    isTopSeller = bool(request.json['isTopSeller'])
    # Create a new book
    new_book = Book(bookTitle, genre, author, ratings, isTopSeller)
    # Add book to the database
    db.session.add(new_book)
    db.session.commit()
    book = {
        "id": new_book.id,
        "bookTitle": new_book.bookTitle,
        "genre": new_book.genre,
        "author": new_book.author,
        "ratings": new_book.ratings,
        "isTopSeller": new_book.isTopSeller
    }
    return json.dumps(book)


# GET A SINGLE BOOK
@app.route('/book/<id>', methods=['GET'])
def book_details(id):
    book = Book.query.get(id)
    my_book = {
        "id": book.id,
        "bookTitle": book.bookTitle,
        "genre": book.genre,
        "author": book.author,
        "ratings": book.ratings,
        "isTopSeller": book.isTopSeller
    }
    return json.dumps(my_book)


# UPDATE A BOOK
@app.route('/bookUpdate/<id>', methods=['PUT'])
def book_update(id):
    book = Book.query.get(id)
    # Received posted data and store it in variables
    bookTitle = request.json['title']
    genre = request.json['genre']
    author = request.json['author']
    ratings = request.json['ratings']
    isTopSeller = request.json['isTopSeller']
    # Add updated book to the database
    db.session.commit()
    updated_book = {
        "bookTitle": book.bookTitle,
        "genre": book.genre,
        "author": book.author,
        "ratings": book.ratings,
        "isTopSeller": book.isTopSeller
    }
    return json.dumps(updated_book)


# DELETE A BOOK
@app.route('/bookDelete/<id>', methods=['DELETE'])
def dele_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    result = "You deleted book " + id
    return result


# RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)


# NOTES

# scrum = Book(title='The scrum guide', description = 'this is a guide to master scrum', author = 'jhon', price = '5')
# db.session.add(scrum)
# db.session.commit()

# >>> from app import db, Book
# >>> db.create_all()
# >>> db.drop_all()

# >>> Book.query.all()
# [<Book 1>, <Book 2>]
# >>> Book.query.get(1)

# [{"author": "SAM", "description": "this is a guide to master scrum", "id": 1, "price": 5, "title": "The scrum guide"},
# {"author": "cohelo", "description": "this is an agile guide", "id": 2, "price": 10, "title": "The agile methodology"},
# {"author": "Mary bett", "description": "computer lenguage", "id": 3, "price": 83, "title": "the bits and bytes"},
# {"author": "Tim ghist", "description": "How data is stored", "id": 4, "price": 103, "title": "the memmory"}, {"author":
# "mecho", "description": "turn obj to json with json.dumps(obj.__dic__)", "id": 5, "price": 6, "title": "jsontest"},
# {"author": "mecho", "description": "turn obj to json with json.dumps(obj.__dic__)", "id": 6, "price": 6, "title":
# "jsontest"}]
