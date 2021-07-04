from flask import (
    Blueprint, session, redirect, url_for, render_template, request, flash
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

        # ToDO surround with try
        # Check username, then password, then if username is taken
        if not username:
            error = 'Username required'
        elif not password:
            error = 'Password required'
        elif User.query.filter_by(username=username).one():
            error = 'Username is taken'

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
    if request.method == 'GET':
        # Process form data
        username = request.form['username']
        password = request.form['password']

        error = None

        # ToDO surround with try
        # Check username and password
        user_query = User.query.filter_by(username=username).one()

        if user_query is None:
            error = 'User does not exist!'
        elif not check_password_hash(user_query['password'], password):
            error = 'Password does not match'

        # Valid form
        if error is None:
            session.clear()
            session['user_id'] = user_query['id']
            return redirect(url_for('index'))

        flash(error)  # Else show error

    return render_template('auth/login.html')


# Logout view
@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('index'))

