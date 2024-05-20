import os

"""
Config class to store all the configuration variables for the application.
SECRET_KEY: Secret key for the application.
SQLALCHEMY_DATABASE_URI: Database URI for the application.
SQLALCHEMY_TRACK_MODIFICATIONS: To disable the modification tracking.
JWT_SECRET_KEY: Secret key for the JWT token.
MAIL_SERVER: SMTP server for sending emails.
MAIL_PORT: Port for the SMTP server.
MAIL_USE_TLS: To use TLS for the SMTP server.
MAIL_USERNAME: Username for the email server.
MAIL_PASSWORD: Password for the email server.
"""


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET') or 'super-secret'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
