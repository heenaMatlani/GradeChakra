import jwt
from flask import current_app
from datetime import datetime, timedelta
from backend.config import Config

def generate_token(email):
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=2),  # Token expires in 2 hours
        'iat': datetime.utcnow(),
        'sub': email
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
