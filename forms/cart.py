from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class CartForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()])
    count = IntegerField(validators=[DataRequired()])
    cart = StringField(validators=[DataRequired()], render_kw={"value": "1"})
    submit = SubmitField()
