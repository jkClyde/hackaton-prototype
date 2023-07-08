from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

#Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                 Length(min=5, max=20)])
    
    firstname = StringField('First Name', validators=[DataRequired(),
                                                 Length(max=20)])

    lastname = StringField('Last Name', validators=[DataRequired(),
                                                 Length(max=20)])
    
    email = StringField('Email',
                         validators=[DataRequired()])
    password = PasswordField('Password', 
                           validators=[DataRequired()]) 
    confirm_password = PasswordField('Confirm Password', 
                           validators=[DataRequired(),EqualTo('password')]) 
    submit = SubmitField('Sign Up')


# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email',
                         validators=[DataRequired()])
    password = PasswordField('Password', 
                           validators=[DataRequired()]) 
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
