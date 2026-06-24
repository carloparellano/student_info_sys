from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Regexp

ID_PATTERN = r'^\d{4}-\d{4}$'


class StudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[
        DataRequired(),
        Regexp(ID_PATTERN, message='Student ID must follow the format YYYY-NNNN (e.g. 2021-1234)')
    ])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    course_code = SelectField('Course', validators=[DataRequired()])
    year_level = SelectField('Year Level', choices=[
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')
    ], validators=[DataRequired()])
    gender = SelectField('Gender', choices=[
        ('Male', 'Male'), ('Female', 'Female')
    ], validators=[DataRequired()])
    student_url = StringField('Student Image URL')
