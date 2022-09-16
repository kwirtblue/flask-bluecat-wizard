from flask_login import LoginManager
from app import app
from models import User

#Create a login manager
login_manager = LoginManager()
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
login_manager.init_app(app)
login_manager.login_view = "/"



