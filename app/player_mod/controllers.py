from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, make_response, jsonify
import json

from app.player_mod.models import Player, PlayerLeaderBoard

player_mod = Blueprint('player', __name__, url_prefix='/player', template_folder='streetview',
                       static_folder='static')


@player_mod.route('/', methods=['GET', 'POST'])
def rank_players():
    return PlayerLeaderBoard.rank_players()


@player_mod.route('/add', methods=['POST'])
def add_score():

    player = request.form
    name = player['name']
    phone = player['phone']
    treasure_id = player['treasure_id']
    time = player['time']
    points = player['points']
    check_player = Player.get_player_details(phone)
    if check_player:
        """
        player exists, check if they have done the hunt before
        """
        if PlayerLeaderBoard.check_player_integrity(treasure_id, check_player.id):
            return make_response(jsonify({'success': False}))

        player_score = PlayerLeaderBoard(treasure_id, time, points, check_player.id)
        player_score.add()

    else:
        player_ = Player(name, phone)
        player_.add()
        return make_response(jsonify({'success': True}))

