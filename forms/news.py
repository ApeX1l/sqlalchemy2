from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    leader_id = StringField('Id лидера', validators=[DataRequired()])
    work = StringField('Количество часов работы', validators=[DataRequired()])
    collaborators = StringField("Участники", validators=[DataRequired()])
    is_finish = BooleanField("Сделана")
    submit = SubmitField('Применить')
