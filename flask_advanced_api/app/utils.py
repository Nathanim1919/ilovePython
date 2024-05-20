from flask import Flask
from flask_jwt_extended import get_jwt_identity
from functools import wraps


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] != role:
                return {'message': "Unauthorized access"}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper