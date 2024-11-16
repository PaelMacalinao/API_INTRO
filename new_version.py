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



if __name__ == "__main__":
    app.run(debug=True)
