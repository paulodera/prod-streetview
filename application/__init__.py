from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


application = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "auth.signin"

application.config.from_object('config')

db = SQLAlchemy(application)

migrate = Migrate(application, db)


@application.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from application.auth_mod.models import Auth
from application.treasure_mod.models import Treasure
from application.player_mod.models import PlayerLeaderBoard
from application.auth_mod.controllers import auth_mod as auth_module
from application.treasure_mod.controllers import treasure_mod as treasure_module
from application.hunt_mod.controllers import hunt_mod as hunt_module
from application.clue_mod.controllers import clue_mod as clue_module
from application.player_mod.controllers import player_mod as player_module


@login_manager.user_loader
def load_user(user_id):
    return Auth.get(user_id)


@application.route('/', methods=['GET'])
def start():
    data = {
        'treasure': Treasure.get_all(),
        'leaderboard': PlayerLeaderBoard.get_player_rankings()
    }
    return render_template('streetview/start.html', data=data)


application.register_blueprint(auth_module)
application.register_blueprint(treasure_module)
application.register_blueprint(hunt_module)
application.register_blueprint(clue_module)
application.register_blueprint(player_module)


db.create_all()
