from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class RegisterTreasure(Form):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=50)]
    )
    time = IntegerField(
        'Time',
        validators=[DataRequired()]
    )
    description = TextAreaField(
        'Description',
        validators=[DataRequired()]
    )
    objective = TextAreaField(
        'Objective',
        validators=[DataRequired()]
    )
    tag_line_1 = StringField(
        'Primary Tag Line',
        validators=[DataRequired(), Length(max=20)]
    )
    tag_line_2 = StringField(
        'Secondary Tag Line',
        validators=[DataRequired(), Length(max=20)]
    )
    
    submit=SubmitField('Submit')
