from flask import Flask
from app.user import User
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager

from dotenv import load_dotenv
import os

# force loading of environment variables
load_dotenv('.flaskenv')


# creating the Flask app object and login manager
app = Flask(__name__)
app.config['SECRET_KEY'] = 'csc330 spring 2021'
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Our mock database of user objects, stored as a dictionary, where the
# key is the user id, and the value is the User object.  Typically, these
# would need
user_db = {'u': User('u', 'u', 'user'), 'a': User('a', 'a', 'admin')}


from app import routes, forms, user
