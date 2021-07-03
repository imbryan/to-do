from flask import Blueprint, session, redirect, url_for

bp = Blueprint('auth', __name__)


# Registration view
@bp.route('/register', methods=('GET', 'POST'))
def register():
    pass


# Login view
@bp.route('/login', methods=('GET', 'POST'))
def login():
    pass


# Logout view
@bp.route('logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('index'))

