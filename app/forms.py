from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=4, max=30)]);

    email = StringField('Email',validators=[DataRequired(), Email()]);

    password = PasswordField('Password', validators=[DataRequired()]);
    confirm_password = PasswordField('Confirm Password', 
                                        validators=[DataRequired(), EqualTo('password')]);
    submit = SubmitField('Sign Up');

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()]);
    password = PasswordField('Password',validators=[DataRequired()]);
    remember = BooleanField('Remember me');
    submit = SubmitField('Login');

class FileUpload(FlaskForm):
    file = FileField('Upload File Instead?', validators=[FileAllowed(['txt'])]);
