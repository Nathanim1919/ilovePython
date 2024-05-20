from crypt import methods
from flask import Blueprint, jsonify, request
from app import db, jwt, mail
from app.model import User, Task
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Message
import pyotp

# Create the routes blueprint
bp = Blueprint('routes', __name__)


@bp.route('/', methods=['GET'])
def index():
    return jsonify({'message': "Welcome to the Flask Advanced API"}), 200


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': "Username and password are required"}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': "User created successfully"}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': "Username and password are required"}), 400
    

    user = User.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'message': "Invalid credentials"}), 401
    
    access_token = create_access_token(identity={'username':user.username, 'role': user.role})
    return jsonify({'access_token': access_token}), 200