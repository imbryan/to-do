from flask import Blueprint, session, redirect, url_for, render_template

bp = Blueprint('auth', __name__)


# Registration view
@bp.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('auth/register.html')


# Login view
@bp.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('auth/login.html')


# Logout view
@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('index'))

