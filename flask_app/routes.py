from flask_app import app, db
import requests
from flask import render_template, flash, redirect, url_for, abort, request
from flask_app.forms import RegistrationForm, LoginForm, TodoForm
from flask_app.models import User, Todo
from flask_login import login_user, logout_user, current_user, login_required
from flask_app import bcrypt
import flask_app.handlers

@app.route('/')
def home():
    return render_template('index.html', title='Home')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('todos'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You have registered successfully.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form, title='Signup')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todos'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('todos'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/todos', methods=['GET', 'POST'])
@login_required
def todos():
    form = TodoForm()

    if form.validate_on_submit():
        task = Todo(title=form.title.data,
                    desc=form.desc.data, status=False, user=current_user)
        db.session.add(task)
        db.session.commit()

    return render_template('todos.html', form=form, title='Todos', complete=Todo.query.filter_by(status=True), incomplete=Todo.query.filter_by(status=False))


@app.route('/todos/<id>/complete')
def complete(id):
    task = Todo.query.get_or_404(id)

    task.status = True
    db.session.commit()

    return redirect(url_for('todos'))


@app.route('/todos/<id>/incomplete')
def incomplete(id):
    task = Todo.query.get_or_404(id)

    task.status = False
    db.session.commit()

    return redirect(url_for('todos'))


@app.route('/todos/<id>/delete')
def todo_delete(id):
    task = Todo.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('todos'))


@app.route('/todos/<id>/update', methods=['GET', 'POST'])
@login_required
def todo_update(id):
    task = Todo.query.get_or_404(id)

    if task.user != current_user:
        abort(403)

    form = TodoForm()

    if form.validate_on_submit():

        task.title = form.title.data
        task.desc = form.desc.data
        db.session.commit()
        flash('Your todo has been updated.', 'success')

        return redirect(url_for('todos'))

    form.title.data = task.title
    form.desc.data = task.desc

    return render_template('todo_update.html', title='Update Todo', form=form)

