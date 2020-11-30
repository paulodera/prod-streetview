from flask import render_template, redirect, flash, g, url_for, Blueprint

from app.treasure_mod.models import Treasure
from app.clue_mod.models import Clue, ClueOptions

hunt_mod = Blueprint('hunt', __name__, url_prefix='/hunt', template_folder='streetview', static_folder='streetview')


@hunt_mod.route('/all', methods=['GET'])
def get_hunts():
    data = Treasure.get_all()
    return render_template('streetview/select_hunt.html', data=data)


@hunt_mod.route('/<string:treasure_id>', methods=['GET', 'POST'])
def start_hunt(treasure_id):
    clue_data = Clue.get_clue(treasure_id)
    treasure_data = Treasure.get_treasure_details(treasure_id)
    options_data = ClueOptions.get_clue_options(clue_data.id)

    data = {
        'clue': clue_data,
        'treasure': treasure_data,
        'options': options_data
    }

    return render_template('streetview/hunt.html', data=data)
