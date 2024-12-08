from flask import request, jsonify
import jwt
from config import Config
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(" ")[1]
            print("token: ",not token)
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

def generate_token(user_id):
    token = jwt.encode({'id': user_id}, Config.SECRET_KEY, algorithm="HS256")
    return token
