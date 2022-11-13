from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, IntegerField, PasswordField, TextAreaField 
from wtforms.validators import Length, DataRequired


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(max=225)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    email = StringField("Team Name", validators=[DataRequired(), Length(min=5, max=255)])
    password = PasswordField('User ID', validators=[DataRequired()])
    submit = SubmitField('Add New User')