from flask import render_template, request, redirect, flash, g, url_for, Blueprint, jsonify, make_response
from flask_login import login_required
from application.clue_mod.models import Clue, ClueOptions
from application.clue_mod.forms import ClueForm, ClueOptionForm
from application.treasure_mod.models import Treasure
# helper function
from application.clue_mod.helpers import save_changes, bool_conversion, save_option
from application import db

clue_mod = Blueprint('clue', __name__, url_prefix='/clue', template_folder='streetview', static_folder='streetview')
# options_mod = Blueprint('option', __name__, url_prefix='/option', template_folder='clue_options', static_folder='dashboard')

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


@clue_mod.route('/options/half-life/<string:treasure_id>', methods=['POST', 'GET'])
def half_life(treasure_id):
    return make_response(jsonify(Clue.return_to_start(treasure_id)))


@clue_mod.route('/', methods=['GET'])
@login_required
def get_clue_page():
    return render_template('clue/clue_table.html')


@clue_mod.route('/all', methods=['POST', 'GET'])
@login_required
def get_clues():
    all_clues = Clue.get_all_clues()
    if all_clues:
        return make_response(jsonify(all_clues), 200)


@clue_mod.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    edit clue
    """
    clue_check = Clue.get_clue_by_id(id)
    if clue_check:
        form = ClueForm(request.form, obj=clue_check)
        
        # update form data
        if request.method == 'POST' and form.validate_on_submit(): 
            save_changes(clue_check, form)
            flash("Update is successfull", "success")
            return redirect('/clue')
        else:
            flash("An error occured while trying to save", "danger")
            return redirect('/clue')
        
        # open clue edit page
        return render_template('/clue/edit_clue.html', form=form)
    
    else:
        # clue not found redirect to clue home route with error msg
        flash("Clue not found", "danger")
        return redirect('/clue')


@clue_mod.route('/new', methods=['GET', 'POST'])
@login_required
def new_clue():
    """
    new clue handler
    """
    form = ClueForm(request.form)
    
    if request.method == 'GET':
        treasures = Treasure.get_clue_treasures()
        form.treasure_id.choices = treasures
        return render_template('/clue/new_clue.html', form=form)
    else:
        if form.validate_on_submit():
            clue = Clue()
            save_changes(clue, form, new=True)
            flash("Clue saved successfully", "success")
            return redirect('/clue')
        else:
            flash('Something went wrong', 'danger')
            return redirect('/clue/new')

"""
Options routes on dashboard
"""
@clue_mod.route('/option/all', methods=['GET'])
def get_all_options():
    """
    fetch clue options to display on dashboard
    """
    all_options = ClueOptions.fetch_all_options()
    if all_options:
        return make_response(jsonify(all_options), 200)


@clue_mod.route('/option', methods=['GET'])
@login_required
def get_options():
    """
    render clue options table
    """
    return render_template('clue_options/option_table.html')


@clue_mod.route('/option/new', methods=['GET', 'POST'])
@login_required
def add_new_option():
    """
    handle new option; render form or post data
    """
     # open new clue option form
    clues = Clue.get_option_clues()
    form = ClueOptionForm(request.form)
    if request.method == 'GET':
        form.clue_id.choices = clues
        return render_template('/clue_options/new_option.html', form=form)

    elif request.method == 'POST' and form.validate_on_submit():
        # save clue option data
        option = ClueOptions()
        save_option(option, form, new=True)
        flash("Clue option saved successfully", "success")
        return redirect('/clue/option')


@clue_mod.route('/option/edit/<string:id>', methods=['POST', 'GET'])
def edit_option(id):
    option_check = ClueOptions.fetch_option_details(id)
    if option_check:
        form = ClueOptionForm(request.form, obj=option_check)
        clues = Clue.get_option_clues()
        form.clue_id.choices = clues

        # update form data
        if request.method == 'POST':
            save_option(option_check, form)
            flash("Update is successful", "success")
            return redirect('/clue/option')
        
        # open clue option edit page
        return render_template('/clue_options/edit_option.html', form=form)
    
    else:
        # clue not found redirect to clue home route with error msg
        flash("Clue option not found", "danger")
        return redirect('/clue/option')

