from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class JobsCreateForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    team_leader = IntegerField('Ответственный(Id)', validators=[DataRequired()])
    work_size = IntegerField('Количество часов', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    is_finished = BooleanField('Завершена')
    submit = SubmitField('Добавить')
