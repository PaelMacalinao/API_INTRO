from flask import Flask, jsonify, request
from http import HTTPStatus
from db import get_db_connection 
app = Flask(__name__)

def fetch_books():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return books
    return []

def fetch_book(book_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        cursor.close()
        conn.close()
        return book
    return None

def add_book(title, author, year):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)",
            (title, author, year)
        )
        conn.commit()
        cursor.close()
        conn.close()

def update_book_info(book_id, title, author, year):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE books SET title = %s, author = %s, year = %s WHERE id = %s",
            (title, author, year, book_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

def delete_book_by_id(book_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        conn.commit()
        cursor.close()
        conn.close()

@app.route("/api/books", methods=["GET"])
def get_books():
    books = fetch_books()
    return jsonify({"success": True, "data": books, "total": len(books)}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = fetch_book(book_id)
    if book is None:
        return jsonify({"success": False, "error": "Book not found"}), HTTPStatus.NOT_FOUND
    return jsonify({"success": True, "data": book}), HTTPStatus.OK

@app.route("/api/books", methods=["POST"])
def create_book():
    if not request.is_json:
        return jsonify({"success": False, "error": "Request must be JSON"}), HTTPStatus.BAD_REQUEST

    data = request.get_json()
    required_fields = ["title", "author", "year"]
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "error": f"Missing required field: {field}"}), HTTPStatus.BAD_REQUEST

    add_book(data["title"], data["author"], data["year"])
    return jsonify({"success": True, "data": data}), HTTPStatus.CREATED

@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = fetch_book(book_id)
    if book is None:
        return jsonify({"success": False, "error": "Book not found"}), HTTPStatus.NOT_FOUND

    data = request.get_json()
    title = data.get("title", book["title"])
    author = data.get("author", book["author"])
    year = data.get("year", book["year"])

    update_book_info(book_id, title, author, year)
    return jsonify({"success": True, "data": {"id": book_id, "title": title, "author": author, "year": year}}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = fetch_book(book_id)
    if book is None:
        return jsonify({"success": False, "error": "Book not found"}), HTTPStatus.NOT_FOUND
    
    delete_book_by_id(book_id)
    return jsonify({"success": True, "message": f"Book with id {book_id} has been deleted."}), HTTPStatus.NO_CONTENT

if __name__ == "__main__":
    app.run(debug=True)
