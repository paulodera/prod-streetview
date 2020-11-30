from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from flask_login import login_user, logout_user, login_required

from werkzeug.security import check_password_hash

from app import db

from app.auth_mod.forms import LoginForm

from app.auth_mod.models import Auth

auth_mod = Blueprint('auth', __name__, url_prefix='/auth', template_folder='template', static_folder='static')


@auth_mod.route('/signin', methods=['POST', 'GET'])
def signin():
    """
    administrator dashboard sign in controller
    :return:
    """
    form = LoginForm(request.form)

    if form.validate_on_submit():

        user = Auth.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):

            login_user(user)

            flash('Welcome %s' % user.username)

            return redirect('/treasure')

        flash('Wrong username and/or password', 'error-message')

    return render_template('auth/signin.html', form=form)


@auth_mod.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('signin')
