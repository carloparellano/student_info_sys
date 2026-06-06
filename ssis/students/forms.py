from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    course_code = SelectField('Course', validators=[DataRequired()])
    year_level = StringField('Year Level', validators=[DataRequired()])
    gender = SelectField(
        'Gender',
        choices=[('Male', 'Male'), ('Female', 'Female')],
        validators=[DataRequired()]
    )
    student_url = StringField('Student Image URL')
