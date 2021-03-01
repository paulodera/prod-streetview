"""
clue helper functions
"""
import uuid
from application import db


def save_changes(clue, form, new=False):
    """
    save new treasure clue
    :param clue:
    :param form:
    :param new:
    :return:
    """
    # convert clue to array
    clue.description = form.description.data
    clue.endpoint = bool_conversion(form.endpoint.data)
    clue.startpoint = bool_conversion(form.startpoint.data)
    clue.slug = form.slug.data.split(",")
    clue.marker_pos = form.marker_pos.data
    clue.is_correct = bool_conversion(form.is_correct.data)
    
    if new:
        clue.id = uuid.uuid4()
        clue.save()
    
    db.session.commit()


def save_option(option, form, new=False):
    """
    save new clue option
    """
    option.name = form.name.data
    option.slug = form.slug.data
    option.coordinates = form.coordinates.data
    option.points = form.points.data
    option.is_correct = bool_conversion(form.is_correct.data)
    
    if new:
        option.id = uuid.uuid4()
        option.save()
    
    db.session.commit()


def bool_conversion(arg):
    if arg == 'False':
        return False
    
    return True