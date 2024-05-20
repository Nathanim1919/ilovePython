from email.policy import default
import bcrypt
from app import db
from datetime import datetime
import bcrypt


# Create the User and Task models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), default='user')
    two_factor_code = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Set the password for the user
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Check the password for the user
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False, default='')
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

    # Serialize the task object to a dictionary. This will be used to convert the task object to a JSON object.
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}