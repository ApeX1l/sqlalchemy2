from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class DepartForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    leader_id = StringField('Id лидера', validators=[DataRequired()])
    members = StringField('Участники', validators=[DataRequired()])
    email = StringField("Почта", validators=[DataRequired()])
    submit = SubmitField('Применить')
