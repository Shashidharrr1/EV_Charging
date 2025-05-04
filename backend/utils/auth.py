from functools import wraps
from flask import request, jsonify
import jwt
from ..config import Config  # Use relative import

def generate_token(user_id):
    """Generate a JWT token for the given user ID"""
    return jwt.encode(
        {'user_id': user_id},
        Config.SECRET_KEY,
        algorithm='HS256'
    )

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'error': 'Token is invalid'}), 401

        return f(current_user_id, *args, **kwargs)
    return decorated

def is_bunk_owner(user_id, bunk_id):
    """Check if the user is the owner of the bunk"""
    # TODO: Implement bunk ownership check
    # For now, return True for testing
    return True