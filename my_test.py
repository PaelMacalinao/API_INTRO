import json
import pytest
from unittest.mock import patch
from new_version import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_books(client):
    mock_books = [{"id": 1, "title": "Test Book", "author": "Author", "year": 2021}]
    
    with patch('new_version.fetch_books', return_value=mock_books):
        response = client.get('/api/books')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert len(data['data']) == 1
    assert data['total'] == 1

def test_get_book(client):
    mock_book = {"id": 1, "title": "Test Book", "author": "Author", "year": 2021}
    
    with patch('new_version.fetch_book', return_value=mock_book):
        response = client.get('/api/books/1')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['data']['id'] == 1

def test_get_book_not_found(client):
    with patch('new_version.fetch_book', return_value=None):
        response = client.get('/api/books/999')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] == False
    assert data['error'] == 'Book not found'

def test_create_book(client):
    mock_book_data = {"title": "New Book", "author": "New Author", "year": 2024}
    
    with patch('new_version.add_book') as mock_add_book:
        response = client.post('/api/books', json=mock_book_data)
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['data']['title'] == 'New Book'
    mock_add_book.assert_called_once_with('New Book', 'New Author', 2024)

def test_create_book_missing_field(client):
    mock_book_data = {"title": "New Book", "author": "New Author"}  
    
    response = client.post('/api/books', json=mock_book_data)
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] == False
    assert data['error'] == 'Missing required field: year'