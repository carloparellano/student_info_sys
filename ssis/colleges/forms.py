from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class CollegeForm(FlaskForm):
    college_code = StringField('College Code', validators=[DataRequired()])
    college_name = StringField('College Name', validators=[DataRequired()])
