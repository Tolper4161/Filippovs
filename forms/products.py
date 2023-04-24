from flask_wtf import FlaskForm
from wtforms import IntegerField, FileField, SubmitField, StringField
from flask_wtf.file import FileRequired
from wtforms.validators import DataRequired


class ProductsForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={"placeholder": "Title"})
    price = IntegerField(validators=[DataRequired()], render_kw={"placeholder": "Price"})
    discription = StringField(validators=[DataRequired()], render_kw={"placeholder": "Discription"})
    picture = FileField(validators=[FileRequired('File was empty!')])
    tags = StringField(validators=[DataRequired()], render_kw={"placeholder": "Tags"})
    submit = SubmitField("add product")
