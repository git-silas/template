from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators
from wtforms.fields.simple import EmailField
from wtforms.validators import Email, InputRequired, Length


class RegisterForm(FlaskForm):

    first_name = StringField(
        'Vorname',
        id='register_firstname',
        validators=[
            InputRequired()
            ]
        )

    last_name = StringField(
        'Nachname',
        id='register_lastname',
        validators=[
            InputRequired()
            ]
        )

    email = EmailField(
        'E-Mail Adresse',
        id='register_email',
        validators=[
            InputRequired(),
            Email()
            ]
        )

    password = PasswordField(
        'Passwort',
        id='register_password',
        validators=[
            InputRequired(),
            Length(min=5)
            ]
        )

    conf_password = PasswordField(
        'Passwort wiederholen',
        id='register_confpassword',
        validators=[
            InputRequired(),
            Length(min=5),
            validators.EqualTo('password', message='Passwörter müssen übereinstimmen')
            ]
        )

    submit = SubmitField(
        'Registrieren',
        id='register_submit',
        )


class LoginForm(FlaskForm):

    email = EmailField(
        'E-Mail Adresse',
        id='login_email',
        validators=[
            InputRequired(),
            Email()
            ]
        )

    password = PasswordField(
        'Passwort',
        id='login_password',
        validators=[
            InputRequired(),
            Length(min=5)
            ]
        )

    submit = SubmitField(
        'Login',
        id='login_login',
        )
