from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class YourForm(FlaskForm):
    text_input = StringField('', validators=[], render_kw={"placeholder": "University URL"})
