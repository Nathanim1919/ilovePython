from crypt import methods
from turtle import title
from flask import Blueprint, jsonify, request
from app import db, jwt, mail
from app.model import User, Task
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Message
import pyotp
from app.utils import role_required

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


@bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user = get_jwt_identity()
    tasks = Task.query.filter_by(user_id = user['id']).all()
    return jsonify([task.serialize() for task in tasks]), 200


@bp.route('/tasks', methods=['POST'])
@jwt_required()
@role_required('user')
def create_task():
    user = get_jwt_identity()
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'message': "Title required"}), 400
    
    task = Task(title=data['title'], description=data.get('description', ''), user_id=user['id'])
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201



@bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('user') # Ensure only users with the 'user' role can update tasks
def update_task(task_id):
    user = get_jwt_identity()
    task = Task.query.get(task_id)
    if task.user_id != user['id']:
        return jsonify({'message':'Permission denied'}), 403
    

    data = request.get_json()
    task.title = data.get('title', task.title) # Update the title
    task.description = data.get('description', task.description)
    task.done = data.get('done', task.done)
    db.session.commit()
    return jsonify(task.to_dict()), 200


@bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('user')
def delete_task(task_id):
    user = get_jwt_identity()
    task = Task.query.get(task_id)
    if task.user_id != user['id']:
        return jsonify({'message':'Permission denied'}), 403
    

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message':'Task deleted successfully'}), 200