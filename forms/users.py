from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={"placeholder": "Username"})
    email = EmailField(validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Password"})
    password_again = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Repeat the password"})
    submit = SubmitField("create")
