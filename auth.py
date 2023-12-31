from peewee import IntegrityError
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_peewee.utils import get_object_or_404
from flask_login import LoginManager, login_user, logout_user, current_user
from orm import *
from app import app

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'

@lm.user_loader
def load_user(user_id): return User.get(user_id)

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=('GET', 'POST'))
def login(error=None):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.get(User.username==username)

        if user is None:
            error = 'incorrect username'
        elif not check_password_hash(user.password, password):
            error = 'incorrect password'

        if error is None:
            login_user(user)
            flash('logged in')
            return redirect(request.args.get('next') or url_for('index'))

        flash(error)

    return render_template('auth/login.html', error=error)

@bp.route('/logout')
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('index'))


@bp.route('/register', methods=('GET', 'POST'))
def register(error=None):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        error = None

        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'

        if error is None:
            try:
                user = User(username=username, password=generate_password_hash(password), email=email, admin=False)
                user.save()
            except IntegrityError:
                error = f"user {username} is already registered"
            else:
                flash(f"registered user {username}")
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html', error=error)

@bp.route('/user/<string:username>')
def user(username):
    user = get_object_or_404(User.select().where(User.username==username))
    models = [moodel.gatherTags() for moodel in Moodel.select().join(User).where(Moodel.user.username==username)]
    return render_template('auth/user.html', user=user, models=models)
