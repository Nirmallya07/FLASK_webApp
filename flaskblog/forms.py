from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm) :

    username = StringField('username', validators = [DataRequired(), Length(min=2, max = 30)])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    confirm_Password = PasswordField('confirm password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        
        

class LoginForm(FlaskForm) :
    # username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) 
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('passsword', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
    
class UpdateForm(FlaskForm) :
    username = StringField('Username', validators=[DataRequired(), Length(max=30, min=2)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    sublit = SubmitField("Update Info")

    def validate_username(self, username) :
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user :
                raise ValidationError("This username is already taken, please try a new username.")

    def validate_email(self, email) :
        if email.data != current_user.email :
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("This email is already in use, plese use a different email.")

