from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    age = IntegerField('Возраст пользователя', validators=[DataRequired()])
    position = StringField('Должность пользователя', validators=[DataRequired()])
    speciality = StringField('Специальность пользователя', validators=[DataRequired()])
    address = StringField('Адрес пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')


class JobForm(FlaskForm):
    job = TextAreaField('Описание работы', validators=[DataRequired()])
    team_leader = IntegerField('id тимлида', validators=[DataRequired()])
    work_size = IntegerField('Продолжительность работы', validators=[DataRequired()])
    collaborators = StringField('Список участников', validators=[DataRequired()])
    submit = SubmitField('Применить')

