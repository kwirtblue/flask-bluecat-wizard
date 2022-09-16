from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    api_token = db.Column(db.String(128))
    system_info = db.Column(db.String(300))
    sys_info_timestamp = db.Column(db.Integer())

    def set_password(self, password_input):
        self.password_hash = generate_password_hash(password_input)
    def set_api_token(self, token):
        self.api_token = token
    def remove_api_token(self):
        self.api_token = None
    def remove_system_info(self):
        self.system_info = None


class HostList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.Integer)


