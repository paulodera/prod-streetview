from flask import render_template, redirect, flash, g, url_for, Blueprint, make_response, jsonify

from application.treasure_mod.models import Treasure
from application.clue_mod.models import Clue, ClueOptions
from application.player_mod.models import PlayerLeaderBoard

hunt_mod = Blueprint('hunt', __name__, url_prefix='/hunt', template_folder='streetview', static_folder='streetview')


@hunt_mod.route('/all', methods=['GET'])
def get_hunts():
    data = {
        'treasure': Treasure.get_active_hunt(),
        'leaderboard': PlayerLeaderBoard.get_player_rankings()
    }
    return render_template('streetview/select_hunt.html', data=data)


@hunt_mod.route('/<string:treasure_id>', methods=['GET', 'POST'])
def start_hunt(treasure_id):
    clue_data = Clue.get_clue(treasure_id)
    treasure_data = Treasure.get_treasure_details(treasure_id)
    options_data = ClueOptions.get_clue_options(clue_data.id)
    landing_coordinates = ClueOptions.get_start_position(clue_data.id)
    pos = landing_coordinates.split(",")
    all_hunts = Treasure.get_all() # to display on the menu
    leaderboard = PlayerLeaderBoard.get_player_rankings()

    data = {
        'clue': clue_data,
        'treasure': treasure_data,
        'options': options_data,
        'hunts': all_hunts,
        'leaderboard': leaderboard,
        'landing_pos': {
            'lat': pos[0],
            'lng': pos[1]
        }
    }

    return render_template('streetview/hunt.html', data=data)
