from flask_wtf import Form #, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, RadioField, IntegerField
from application.treasure_mod.models import Treasure
from application.clue_mod.models import Clue
from wtforms.validators import DataRequired


class ClueForm(Form):
    """
    clue add and edit form
    """
    treasure_id = SelectField(
        'Treasure',
        choices=Treasure.get_clue_treasures(),
        validators = [DataRequired()]
    )
    description = TextAreaField(
        'Description',
        validators = [DataRequired()]
    )
    startpoint = RadioField(
        'Startpoint',
         choices=[('True', 'Yes'), ('False', 'No')]
    )
    endpoint = RadioField(
        'Endpoint',
        choices=[('True', 'Yes'), ('False', 'No')]
    )
    marker_pos = StringField(
        'Clue Coordinates',
        validators=[DataRequired()]
    )
    is_correct = RadioField(
        'Is this path correct',
         choices=[('True', 'Yes'), ('False', 'No')]
    )
    is_bonus = RadioField(
        'Bonus path',
         choices=[('True', 'Yes'), ('False', 'No')]
    )
    slug = StringField(
        'Clue slugs',
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')


class ClueOptionForm(Form):
    """
    clue options
    """
    clue_id = SelectField(
        'Clue',
        choices=Clue.get_option_clues(),
        validators = [DataRequired()] 
    )
    name = StringField(
        'Name',
        validators = [DataRequired()]
    )
    slug = StringField(
        'Slug',
        validators = [DataRequired()]
    )
    coordinates = StringField(
        'Map Coordinates',
        validators = [DataRequired()]
    )
    points = IntegerField(
        'Points',
        validators = [DataRequired()]
    )
    is_correct = RadioField(
        'Is this point correct',
        choices = [(True, 'True'), (False, 'False')]
    )

    submit = SubmitField('Submit')
