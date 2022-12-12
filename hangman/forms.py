from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    email = StringField("Email", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])
    password_confirmation = PasswordField(
        "Repeat password", [EqualTo("password", "passwords must match")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Log in")


class ProfileUpdateForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    picture = FileField('Choose a new profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Confirm')
