from flask import Flask, jsonify, request
from flask_restx import Api, Namespace, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db
from routes.books import books_ns
from routes.members import members_ns

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

jwt = JWTManager(app)

api = Api(app, title="Library Management System API", version="1.0", description="A Flask API for managing books and members")
api.add_namespace(books_ns, path='/books')
api.add_namespace(members_ns, path='/members')

STATIC_USERNAME = "admin"
STATIC_PASSWORD = "admin"

login_ns = Namespace('login', description="Login operations")

@login_ns.route('/')
class Login(Resource):
    def post(self):
        data = request.json
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"message": "Username and password are required"}), 400

        if data['username'] == STATIC_USERNAME and data['password'] == STATIC_PASSWORD:
            access_token = create_access_token(identity=STATIC_USERNAME)
            print("token: ", access_token)
            return {"access_token": access_token}, 200

        return jsonify({"message": "Invalid credentials"}), 401

api.add_namespace(login_ns, path='/login')

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome, {current_user}!"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
