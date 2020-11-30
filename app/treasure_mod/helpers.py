"""
treasure hunt helper functions
"""

from app.treasure_mod.models import Treasure


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

    if new:
        Treasure.save(treasure)
