import pytest
import sys
import os
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Member

STATIC_USERNAME = "admin"
STATIC_PASSWORD = "admin"
SECRET_KEY = os.getenv('SECRET_KEY')

def create_jwt_token(username):
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    token = jwt.encode(
        {'username': username, 'exp': expiration_time}, SECRET_KEY , algorithm="HS256"
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
def auth_token(client):
    return create_jwt_token(STATIC_USERNAME)

def test_get_members(client, auth_token):
    with app.app_context():
        member1 = Member(name="John Doe", email="john.doe@example.com", membership_date="2023-01-01")
        member2 = Member(name="Jane Smith", email="jane.smith@example.com", membership_date="2023-02-01")
        db.session.add_all([member1, member2])
        db.session.commit()

    response = client.get('/members', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = response.json
    assert len(data['items']) == 2

def test_create_member(client, auth_token):
    response = client.post('/members', json={
        'name': 'Alice Wonderland',
        'email': 'alice.wonderland@example.com',
        'membership_date': '2023-03-01',
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 201
    data = response.json
    assert data['name'] == 'Alice Wonderland'
    assert data['email'] == 'alice.wonderland@example.com'

def test_update_member(client, auth_token):
    with app.app_context():
        member = Member(name="Old Name", email="old.email@example.com", membership_date="2023-01-01")
        db.session.add(member)
        db.session.commit()

        member = db.session.query(Member).get(member.id)

    response = client.put(f'/members/{member.id}', json={
        'name': 'Updated Name',
        'email': 'updated.email@example.com',
        'membership_date': '2023-05-01'
    }, headers={
        'Authorization': f'Bearer {auth_token}'
    })

    assert response.status_code == 200
    updated_member = db.session.query(Member).get(member.id)
    assert updated_member.name == 'Updated Name'
    assert updated_member.email == 'updated.email@example.com'
    assert updated_member.membership_date == '2023-05-01'

def test_delete_member(client, auth_token):
    with app.app_context():
        member = Member(name="Delete Me", email="delete.me@example.com", membership_date="2023-01-01")
        db.session.add(member)
        db.session.commit()

        member = db.session.query(Member).get(member.id)

    response = client.delete(f'/members/{member.id}', headers={      
        'Authorization': f'Bearer {auth_token}'
    })

    assert response.status_code == 204

    deleted_member = db.session.query(Member).get(member.id)
    assert deleted_member is None