from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import sys


# User class, subclassed from UserMixin for convenience.  UserMixin
# provides attributes to manage user (e.g. authenticated).  The User
# class defines a "role" attribute that represents the user role (e.g.  Regular
# user or admin)
class User(UserMixin):
    def __init__(self, username, password, role):
        self.id = username
        # hash the password and output it to stderr
        self.pass_hash = generate_password_hash(password)
        print(self.pass_hash, file=sys.stderr)
        self.role = role
