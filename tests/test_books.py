import pytest
import sys
import os
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Book

STATIC_USERNAME = "admin"
STATIC_PASSWORD = "admin"

def create_jwt_token(username, password):
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    token = jwt.encode(
        {'username': username, 'exp': expiration_time},  
        os.getenv('SECRET_KEY'),
        algorithm="HS256"
    )
    return token


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    with app.test_client() as client:
        with app.app_context():  
            db.create_all()  
        yield client
        with app.app_context():
            db.drop_all()  


@pytest.fixture
def auth_token():
    return create_jwt_token(STATIC_USERNAME, STATIC_PASSWORD)


def test_get_books(client, auth_token):
    with app.app_context():  
        book1 = Book(title="Book One", author="Author One", published_date="2023")
        book2 = Book(title="Book Two", author="Author Two", published_date="2024")
        db.session.add_all([book1, book2])
        db.session.commit()

    response = client.get('/books', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = response.json
    assert 'items' in data
    assert len(data['items']) == 2


def test_create_book(client, auth_token):
    with app.app_context():  
        response = client.post('/books', json={
            'title': 'New Book',
            'author': 'New Author',
            'published_date': '2025',
        }, headers={
            'Authorization': f'Bearer {auth_token}'
        })
        assert response.status_code == 201
        data = response.json
        assert data['title'] == 'New Book'
        assert data['author'] == 'New Author'

def test_update_book(client, auth_token):
    with app.app_context():
        book = Book(title="Old Book", author="Old Author", published_date="2020")
        db.session.add(book)
        db.session.commit()

        db.session.refresh(book)

        updated_data = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'published_date': '2025'
        }

        response = client.put(f'/books/{book.id}', json=updated_data, headers={
            'Authorization': f'Bearer {auth_token}'
        })
        
        assert response.status_code == 200
        data = response.json
        assert data['title'] == 'Updated Book'
        assert data['author'] == 'Updated Author'
        assert data['published_date'] == '2025'


def test_delete_book(client, auth_token):
    with app.app_context():
        book = Book(title="Book to Delete", author="Author to Delete", published_date="2020")
        db.session.add(book)
        db.session.commit()

        db.session.refresh(book)

        response = client.delete(f'/books/{book.id}', headers={
            'Authorization': f'Bearer {auth_token}'
        })
        
        assert response.status_code == 204

        deleted_book = Book.query.get(book.id)
        assert deleted_book is None
