from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import login_required

from application import db
from application.treasure_mod.models import Treasure

from application.treasure_mod.tables import TreasureTable
from application.treasure_mod.forms import RegisterTreasure

# helper function
from application.treasure_mod.helpers import save_changes

treasure_mod = Blueprint('treasure', __name__, url_prefix='/treasure', template_folder='treasure',
                         static_folder='static')


@treasure_mod.route('/new', methods=['GET', 'POST'])
@login_required
def new_treasure():
    """
    add a new treasure
    :return:
    """
    form = RegisterTreasure(request.form)
    if request.method == 'GET':
        return render_template('treasure/new_treasure.html', form=form)
    else:
        if form.validate_on_submit():
            treasure = Treasure()
            save_changes(treasure, form, new=True)
            flash('Treasure saved successfully', 'success')
            return redirect('/treasure')
        else:
            flash('Something went wrong', 'danger')
            return redirect('/treasure/new')


@treasure_mod.route('/', methods=['GET', 'POST'])
@login_required
def treasures():
    all_treasures = Treasure.get_all()

    if not all_treasures:

        flash("No results were found")
        return render_template('treasure/dashboard.html')
    else:

        table = TreasureTable(all_treasures)
        return render_template('treasure/dashboard.html', table=table)


@treasure_mod.route('/activate/<string:id>', methods=['GET'])
@login_required
def activate(id):
    treasure_check = Treasure.get_treasure(id)
    
    if not treasure_check:
        flash("Treasure not found", "danger")
        return redirect('/treasure')

    if treasure_check.is_active == False and bool(Treasure.get_active_hunt()) == True:
        flash("Only one hunt may be active at a time", "danger")
        return redirect('/treasure')
    elif treasure_check.is_active:
        treasure_check.update({'is_active': False})
    else:
        treasure_check.update({'is_active': True})
    
    flash("Status updated successfully", "success")
    return redirect('/treasure')


@treasure_mod.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    treasure_check = Treasure.get_treasure(id)

    if treasure_check:
        form = RegisterTreasure(request.form, obj=treasure_check)
        # return form on another page
        if request.method == 'POST' and form.validate_on_submit():
            save_changes(treasure_check, form)
            flash("Update successfull", "success")
            return redirect('/treasure')

        return render_template('/treasure/edit_treasure.html', form=form)

    else:
        flash("Treasure not found", "danger")
        return redirect('/treasure')


# @treasure_mod.route('/edit', methods=['POST'])
# @login_required
# def edit_form():
#     form = RegisterTreasure(request.form)
#     treasure_check = Treasure.get_treasure(form.id.data)

#     if treasure_check:
#         # validate and update data
#         if form.validate_on_submit():
           
#         else:
#             flash_errors(form)
#             return redirect('/treasure')
#     else:
#         flash("Treasure not found", "danger")
#         return redirect('/treasure')
