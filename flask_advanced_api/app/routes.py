from crypt import methods
from random import randint
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
    user.role = data.get('role', 'user')
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
    
    access_token = create_access_token(identity={'username':user.username, 'role': user.role, 'id': user.id})
    return jsonify({'access_token': access_token}), 200


@bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user = get_jwt_identity()
    tasks = Task.query.filter_by(user_id = user['id']).all()
    return jsonify([task.serialize() for task in tasks]), 200


@bp.route('/tasks', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_task():
    user = get_jwt_identity()
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'message': "Title required"}), 400
    
    task = Task(title=data['title'], description=data.get('description'), user_id=user['id'])
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




# Two-factor authentication
@bp.route('/send_sfa_code', methods=['POST'])
@jwt_required()
def send_2fa_code():
    user = get_jwt_identity()
    user = User.query.get(user['id']).first()


    if not user:
        return jsonify({'message': "User not found"}), 404
    

    # Generate the 2FA secret key
    user.two_factor_code = randint(100000, 999999)
    db.session.commit()


    # Send the 2FA code to the user's email
    msg = Message('Your 2FA Code', recipients=[user.email])
    msg.body = f"Your 2FA code is {user.two_factor_code}"
    mail.send(msg)


    return jsonify({'message': "2FA code sent successfully"}), 200



# Verify the 2FA code
@bp.route('/verify_2fa_code', methods=['POST'])
@jwt_required()
def verify_2fa_code():
    user = get_jwt_identity()
    user = User.query.get(user['id']).first()


    data = request.get_json()
    if not data or not data.get('code'):
        return jsonify({'message': "2FA code required"}), 400
    

    if user.two_factor_code != data['code']:
        return jsonify({'message': "Invalid 2FA code"}), 401
    

    user.two_factor_code = None
    db.session.commit()


    return jsonify({'message': "2FA code verified successfully"}), 200


# Add the error handler for the 404 error
@bp.errorhandler(404)
def not_found_error(error):
    return jsonify({'message': "Resource not found"}), 404
