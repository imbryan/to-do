from flask import Flask, redirect, url_for, render_template, request, session, g, flash
from models import db, User, ToDO
from decouple import config
from auth import bp as auth_bp
from werkzeug.exceptions import abort

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)
db.create_all()


@app.route("/", methods=('GET', 'POST'))
def index():
    # handle forms
    if request.method == 'POST':
        # user must be logged
        if g.user:
            new_todo_text = request.form['new']

            # if there is text present
            if new_todo_text:
                new_todo = ToDO(text=new_todo_text, user_id=session['user_id'])
                db.session.add(new_todo)
                db.session.commit()
        # return redirect for all post requests
        return redirect(url_for('index'))

    # the following handles GET requests
    todos = None
    try:
        todos = ToDO.query.filter_by(user_id=session['user_id'], complete=False).all()
    except Exception:
        pass  # No to-do's found

    return render_template('index.html', todos=todos)


@app.route('/<int:id>/change', methods=('POST',))
def change(id):
    if request.method == 'POST':
        todo = ToDO.query.filter_by(id=id).one()

        # You may only change your own todos
        if todo.user_id is not session['user_id']:
            abort(403)
        else:
            if 'delete' in request.form:
                ToDO.query.filter_by(id=id).delete()
            elif 'update' in request.form:
                todo.text = request.form['todotext']
            elif 'complete' in request.form:
                todo.complete = True

            db.session.commit()

    return redirect(url_for('index'))


# Authentication Blueprint
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(port=3000)
