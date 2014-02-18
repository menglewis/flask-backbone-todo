from flask import jsonify, render_template, request, flash, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from models import TodoItem, User
from forms import LoginForm, RegisterForm

@app.route('/')
@login_required
def index():
    todos = [i.serialize() for i in TodoItem.query.filter_by(
            user_id=current_user.id)]
    return render_template('index.html', todos=todos)

@app.route('/todos/', methods=['POST'])
@login_required
def todo_create():
    todo = request.get_json()
    new_todo = TodoItem(title = todo['title'],
            completed = todo['completed'],
            order = todo['order'],
            user_id = current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.serialize())

@app.route('/todos/<int:id>', methods=['GET'])
@login_required
def todo_get(id):
    todo = TodoItem.query.get(id)
    return jsonify(todo.serialize())

@app.route('/todos/<int:id>', methods=['PUT', 'PATCH'])
@login_required
def todo_update(id):
    new_todo = request.get_json()
    todo = TodoItem.query.filter_by(id=id, user_id=current_user.id).first()
    todo.title, todo.completed, todo.order = (new_todo['title'], 
        new_todo['completed'], new_todo['order'])
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.serialize())

@app.route('/todos/<int:id>', methods=['DELETE'])
@login_required
def todo_delete(id):
    todo = TodoItem.query.filter_by(id=id, user_id=current_user.id).first()
    db.session.delete(todo)
    db.session.commit()
    return jsonify({})

@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
            password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Thank you for registering.", 'success')
        login_user(new_user)
        return redirect(url_for('index'))
    else:
        flash_errors(form)
    return render_template('register.html', form=form)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            return redirect(url_for("index"))
        else:
            flash_errors(form)
    return render_template("login.html", form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)