from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from werkzeug.security import check_password_hash

from app import db

from app.auth_mod.forms import LoginForm

from app.auth_mod.models import Auth

auth_mod = Blueprint('auth', __name__, url_prefix='/auth', template_folder='template', static_folder='static')


@auth_mod.route('/signin', methods=['POST', 'GET'])
def signin():

    form = LoginForm(request.form)

    if form.validate_on_submit():

        user = Auth.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):

            session['user_id'] = user.id

            flash('Welcome %s' % user.username)

            return redirect(url_for('auth.dashboard'))

        flash('Wrong username and/or password', 'error-message')

    return render_template('auth/signin.html', form=form)