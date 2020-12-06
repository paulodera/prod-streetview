from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.signin"

app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from app.auth_mod.models import Auth
from app.treasure_mod.models import Treasure
from app.auth_mod.controllers import auth_mod as auth_module
from app.treasure_mod.controllers import treasure_mod as treasure_module
from app.hunt_mod.controllers import hunt_mod as hunt_module
from app.clue_mod.controllers import clue_mod as clue_module


@login_manager.user_loader
def load_user(user_id):
    return Auth.get(user_id)


@app.route('/', methods=['GET'])
def start():
    data = Treasure.get_all()
    return render_template('streetview/start.html', data=data)


app.register_blueprint(auth_module)
app.register_blueprint(treasure_module)
app.register_blueprint(hunt_module)
app.register_blueprint(clue_module)


db.create_all()
