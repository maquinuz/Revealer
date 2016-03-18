from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password', category='warning')

    return render_template('auth/login.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", category='info')
    return redirect(url_for('index'))


@auth.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        login_user(user)
        return redirect(url_for('index'))
    return render_template('auth/register.html', form=form)
