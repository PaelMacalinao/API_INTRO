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

def test_update_book(client):
    mock_existing_book = {"id": 1, "title": "Test Book", "author": "Author", "year": 2021}
    updated_data = {"title": "Updated Book", "author": "Updated Author", "year": 2024}
    
    with patch('new_version.fetch_book', return_value=mock_existing_book), \
         patch('new_version.update_book_info') as mock_update:
        response = client.put('/api/books/1', json=updated_data)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['data']['title'] == 'Updated Book'
    mock_update.assert_called_once_with(1, 'Updated Book', 'Updated Author', 2024)

def test_update_book_not_found(client):
    with patch('new_version.fetch_book', return_value=None):
        response = client.put('/api/books/999', json={"title": "Updated Book"})
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] == False
    assert data['error'] == 'Book not found'

def test_delete_book(client):
    mock_existing_book = {"id": 1, "title": "Test Book", "author": "Author", "year": 2021}
    
    with patch('new_version.fetch_book', return_value=mock_existing_book), \
         patch('new_version.delete_book_by_id') as mock_delete:
        response = client.delete('/api/books/1')
    
    assert response.status_code == 204
    assert response.data == b''  
    mock_delete.assert_called_once_with(1)

def test_delete_book_not_found(client):
    with patch('new_version.fetch_book', return_value=None):
        response = client.delete('/api/books/999')
    
    assert response.status_code == 404
    data = json.loads(response.data) if response.data else {}
    assert data.get('success', False) == False
    assert data.get('error') == 'Book not found'  
