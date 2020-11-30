from flask import render_template, redirect, flash, g, url_for, Blueprint, jsonify, make_response

from app.clue_mod.models import Clue, ClueOptions

clue_mod = Blueprint('clue', __name__, url_prefix='/clue', template_folder='streetview', static_folder='streetview')


@clue_mod.route('/options/<string:option_id>', methods=['POST', 'GET'])
def get_clue_options(option_id):
    option_details = ClueOptions.get_clue_details(option_id)
    return make_response(jsonify(option_details))


@clue_mod.route('/options/<string:treasure_id>/<string:slug>', methods=['POST', 'GET'])
def get_next_clue(treasure_id, slug):
    next_clue = Clue.get_next_clue(slug, treasure_id)
    if next_clue:
        return make_response(jsonify(next_clue))
    else:
        return make_response(jsonify({'404': 'not found'}))

