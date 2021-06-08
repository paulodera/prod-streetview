from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

application = Flask(__name__)

content_policies = {
    'default-src': [
        '\'self\'',
        '*.bootstrapcdn.com',   
    ],
    'script-src': [
        '\'self\'',
        '\'unsafe-eval\'',
        '\'unsafe-inline\'',
        'sha256-56unDXjk2ShFPvYp44q8qpaNjzpU2ut/TGooXPhreOk=',
        'cdnjs.cloudflare.com',
        'maps.googleapis.com',
        'maps.gstatic.com',
    ],
    'img-src': [
        'data:',
        '*',
        '\'unsafe-eval\'',
    ],
    'style-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'fonts.googleapis.com',
        'maxcdn.bootstrapcdn.com'
    ],
    'object-src':'\'self\'',
    'font-src': [
        '\'self\'',
        'fonts.googleapis.com',
        'fonts.gstatic.com',
        'maxcdn.bootstrapcdn.com'
    ],
    'connect-src': [
        '\'self\'',
        '*.google-analytics.com'
    ]
}
Talisman(application, content_security_policy=content_policies)


login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "auth.signin"

# csrf protection
csrf = CSRFProtect(application)
csrf.init_app(application)

application.config.from_object('config')

db = SQLAlchemy(application)

migrate = Migrate(application, db)


@application.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from application.auth_mod.models import Auth
from application.treasure_mod.models import Treasure
from application.clue_mod.models import Clue
from application.clue_mod.models import ClueOptions
from application.player_mod.models import Player
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

# if __name__ == '__main__':
#     db.create_all()-
#     application.run(host='0.0.0.0')