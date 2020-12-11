from flask import render_template, redirect, flash, g, url_for, Blueprint, make_response, jsonify, request, escape
from app.player_mod.models import Player, PlayerLeaderBoard
from app.treasure_mod.models import Treasure
from app import db


player_mod = Blueprint('player',
                       __name__,
                       url_prefix='/player',
                       template_folder='streetview',
                       static_folder='streetview'
                       )


@player_mod.route('/register', methods=['POST'])
def register_new_player():
    """
    register new player
    :return:
    """
    phone = escape(request.form.get('phone'))
    username = escape(request.form.get('username'))
    time = escape(request.form.get('time'))
    points = escape(request.form.get('points'))
    treasure_id = escape(request.form.get('treasure_id'))

    # check whether the current treasure data is active
    if not Treasure.check_hunt_status(treasure_id):
        msg = {
            'status': 1,
            'message': 'This hunt is unavailable'
        }
        return make_response(jsonify(msg))

    # check if the player exists
    player_details = Player.check_player_details(phone)
    if not player_details:
        new_player = Player(username, phone)
        new_player.save()
        new_score = PlayerLeaderBoard(treasure_id, time, points, new_player.id)
        new_score.save()
        msg = {
            'status': 0,
            'message': 'Thank you for playing'
        }
        return make_response(jsonify(msg))

    if not PlayerLeaderBoard.check_play_status(player_details.id, treasure_id):
        # save score details if the player has not played the hunt before
        new_score = PlayerLeaderBoard(treasure_id, time, points, player_details.id)
        new_score.save()
        msg = {
            'status': 0,
            'message': 'Thank you for playing'
        }
        return make_response(jsonify(msg))

    msg = {
        'status': 1,
        'message': 'You can only participate once'
    }
    return make_response(jsonify(msg))
