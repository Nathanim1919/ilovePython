from flask import Flask
from flask_jwt_extended import get_jwt_identity
from functools import wraps


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user = get_jwt_identity()
            print(f"Current user role: {current_user['role']}")  # Debugging
            if current_user['role'] != role:
                print(f"Unauthorized access: {current_user['role']}")
                return {'message': "Unauthorized access"}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper