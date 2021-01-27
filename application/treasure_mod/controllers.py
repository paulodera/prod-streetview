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


@treasure_mod.route('/new')
@login_required
def new_treasure():
    """
    add new treasure
    :return:
    """

    form = RegisterTreasure(request.form)

    if form.validate_on_submit():

        treasure = Treasure()
        save_changes(treasure, form, new=True)
        flash('Treasure saved successfully')
        return redirect('/treasure')

    return render_template('treasure/new_treasure.html', form=form)


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

