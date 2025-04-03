from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class JobsCreateForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    team_leader = IntegerField('Ответственный(Id)', validators=[DataRequired()])
    work_size = IntegerField('Количество часов', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    is_finished = BooleanField('Завершена')
    categories = MultiCheckboxField('Категории', coerce=int)
    submit = SubmitField('Сохранить')
