from flask import (
    Blueprint, session, redirect, url_for, render_template, request, flash, g
    )
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__)


# Registration view
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # Process form data
        username = request.form['username']
        password = request.form['password']

        error = None

        # Check username, then password, then if username is taken
        if not username:
            error = 'Username required'
        elif not password:
            error = 'Password required'

        try:
            if User.query.filter_by(username=username).one():
                error = 'Username is taken'
        except Exception:
            pass  # User does not exist

        # Valid form
        if error is None:
            new_user = User(
                username=username,
                password=generate_password_hash(password),
            )

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)  # Else show error

    return render_template('auth/register.html')


# Login view
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # Process form data
        username = request.form['username']
        password = request.form['password']

        error = None

        # Check username and password
        try:
            user = User.query.filter_by(username=username).one()
        except Exception:
            user = None

        if user is None:
            error = 'User does not exist!'
        elif not check_password_hash(user.password, password):
            error = 'Password does not match'

        # Valid form
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)  # Else show error

    return render_template('auth/login.html')


# Logout view
@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('index'))


# Pass user to g object
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).one()
