from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.signin"

app.config.from_object('config')

db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from app.auth_mod.models import Auth
from app.auth_mod.controllers import auth_mod as auth_module


@login_manager.user_loader
def load_user(user_id):
    return Auth.get(user_id)


app.register_blueprint(auth_module)

db.create_all()
