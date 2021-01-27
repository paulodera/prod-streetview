from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class RegisterTreasure(Form):
    """
    new treasure hunt entry
    """
    name = StringField(
        'Hunt name',
        validators=[DataRequired()]
    )
    description = TextAreaField(
        'Hunt description'
    )
    time = IntegerField(
        'Total time',
        validators=[DataRequired()]
    )
    submit = SubmitField('Add Treasure')

