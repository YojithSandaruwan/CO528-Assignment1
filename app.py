from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory database of books
books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "published_year": 1949},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "published_year": 1960},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "published_year": 1925},
]

# Helper function to find a book by id
def find_book(book_id):
    return next((book for book in books if book['id'] == book_id), None)

# Create a new book (POST)
@app.route('/books', methods=['POST'])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    new_book = {
        "id": books[-1]["id"] + 1 if books else 1,
        "title": request.json.get("title"),
        "author": request.json.get("author", "Unknown"),
        "published_year": request.json.get("published_year", None),
    }
    books.append(new_book)
    return jsonify(new_book), 201

# Retrieve all books (GET)
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# Retrieve a single book by id (GET)
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = find_book(book_id)
    if book is None:
        abort(404)
    return jsonify(book)

# Update an existing book (PUT)
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = find_book(book_id)
    if book is None:
        abort(404)
    if not request.json:
        abort(400)
    book["title"] = request.json.get("title", book["title"])
    book["author"] = request.json.get("author", book["author"])
    book["published_year"] = request.json.get("published_year", book["published_year"])
    return jsonify(book)

# Delete a book by id (DELETE)
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = find_book(book_id)
    if book is None:
        abort(404)
    books.remove(book)
    return jsonify({"result": True})

if __name__ == '__main__':
    app.run(debug=True)
