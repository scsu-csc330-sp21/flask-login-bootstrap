from flask import render_template, flash, redirect, url_for, request, Flask
from flask_login import LoginManager, login_user, logout_user, \
    current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash, generate_password_hash
import sys

from app import app, login_manager, user_db
from app.forms import LoginForm



# Login manager uses this function to manage user sessions.
# Function does a lookup by id and returns the User object if
# it exists, None otherwise.
@login_manager.user_loader
def load_user(id):
    return user_db.get(id)

# Helper function that returns True if logged in user has
# "admin" role, False otherwise.
def is_admin():
    if current_user:
        if current_user.role == 'admin':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', name=current_user.id)

# This mimics a situation where a non-admin user attempts to access
# an admin-only area.  @login_required ensures that only authenticated
# users may access this route.
@app.route('/admin_only')
@login_required
def admin_only():
    # determine if current user is admin
    if is_admin():
        return render_template('admin.html', message="I am admin.")
    else:
        return render_template('unauthorized.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # display the login form
    form = LoginForm()
    if form.validate_on_submit():
        user = user_db[form.username.data]
        # validate user
        valid_password = check_password_hash(user.pass_hash, form.password.data)
        if user is None or not valid_password:
            print('Invalid username or password', file=sys.stderr)
            redirect(url_for('index'))
        else:
            login_user(user)
            return redirect(url_for('success'))

    return render_template('login.html', title='Sign In', form=form)

# logging out is managed by login manager
# Log out option appears on the navbar only after a user logs on
# successfully (see lines 25-29 of templates/base.html )
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
