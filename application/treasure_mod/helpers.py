"""
treasure hunt helper functions
"""
import uuid
from application.treasure_mod.models import Treasure
from application import db


def save_changes(treasure, form, new=False):
    """
    save new treasure
    :param treasure:
    :param form:
    :param new:
    :return:
    """
    treasure.name = form.name.data
    treasure.time = form.time.data
    treasure.description = form.description.data
    treasure.objective = form.objective.data
    treasure.tag_line_1 = form.tag_line_1.data
    treasure.tag_line_2 = form.tag_line_2.data

    if new:
        treasure.id = uuid.uuid4()
        treasure.save()
    
    db.session.commit()
