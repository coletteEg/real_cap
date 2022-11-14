from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, IntegerField, PasswordField, TextAreaField 
from wtforms.validators import DataRequired,Email,EqualTo,Length
from model import User, Shark 


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class UserForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Length(min=5, max=255)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add New User')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has an account already')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Choose a new username')

class AddShark(FlaskForm):

    name = StringField('Name of shark: ')
    submit = SubmitField('Request Shark')