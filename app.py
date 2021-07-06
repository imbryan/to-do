from flask import Flask, redirect, url_for, render_template, request, session, g
from models import db, ToDO
from decouple import config
from auth import bp as auth_bp
from werkzeug.exceptions import abort
import datetime

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
                num_todos = ToDO.query.filter_by(complete=False).count()
                new_todo = ToDO(text=new_todo_text, user_id=session['user_id'], position=num_todos+1)
                db.session.add(new_todo)
                db.session.commit()
        # return redirect for all post requests
        return redirect(url_for('index'))

    # the following handles GET requests

    todos = None
    completed_todos = None
    try:
        todos = ToDO.query.filter_by(user_id=session['user_id'], complete=False).order_by(ToDO.position).all()
        completed_todos = ToDO.query.filter_by(user_id=session['user_id'], complete=True).all()
    except Exception:
        pass  # No to-do's found

    return render_template('index.html', todos=todos, complete=completed_todos)


def shuffle(pos):
    num_todos = ToDO.query.filter_by(complete=False).count()  # count number of todos

    current_position = 0 + pos  # the position that has been made empty

    # from the newly vacant position, all todos below will be moved up by 1 position
    try:
        while current_position <= num_todos:  # until all remaining todos are shuffled up
            current_todo = ToDO.query.filter_by(position=current_position+1).one()  # get to-do from below vacant spot
            current_todo.position = current_position  # move to-do into vacant spot
            current_position += 1  # move on to the next vacant spot
            db.session.commit()
    except Exception:
        return redirect(url_for('index'))  # if there are no todos


@app.route('/<int:id>/change', methods=('POST',))
def change(id):
    if request.method == 'POST':
        todo = None
        try:
            todo = ToDO.query.filter_by(id=id).one()
        except Exception:
            return redirect(url_for('index'))  # you shouldn't be on change view

        # You may only change your own todos
        if todo.user_id is not session['user_id']:
            abort(403)
        else:
            # Delete button was pressed
            if 'delete' in request.form:
                pos = 0 + todo.position
                ToDO.query.filter_by(id=id).delete()

                shuffle(pos)
            # Update button was pressed
            elif 'update' in request.form:
                # Update text
                todo.text = request.form['todotext']

                # Update date
                if request.form['date']:
                    date_text = request.form['date'].split('-')
                    new_date = datetime.date(year=int(date_text[0]), month=int(date_text[1]), day=int(date_text[2]))

                    todo.due_date = new_date
            # Mark Complete button was pressed
            elif 'complete' in request.form:
                todo.complete = True  # mark as complete
                shuffle(todo.position)

                todo.position = -1  # all complete todos will be at position -1

            # Mark Incomplete button was pressed
            elif 'restore' in request.form:
                num_todos = ToDO.query.filter_by(complete=False).count()
                todo.complete = False

                todo.position = num_todos+1
            # Move item up the list
            elif 'up' in request.form:
                if todo.position > 1:
                    above_todo = ToDO.query.filter_by(position=todo.position-1).one()
                    above_todo.position += 1

                    todo.position -= 1
            # Move item down the list
            elif 'down' in request.form:
                num_todos = ToDO.query.filter_by(complete=False).count()

                if todo.position < num_todos:
                    below_todo = ToDO.query.filter_by(position=todo.position+1).one()
                    below_todo.position -= 1

                    todo.position += 1

            db.session.commit()

    return redirect(url_for('index'))


# Authentication Blueprint
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(port=3000)
