from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app import db, models


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message='Please enter your name')])
    email = StringField("Email", validators=[DataRequired('Please enter your email'), Email(message="Not a valid "
                                                                                                    "email address")])
    subject = StringField("Subject")
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=4, message="Your message is too short")])
    # recaptcha = RecaptchaField()
    submit = SubmitField("Send")
# [DataRequired(), Email(message='Not a valid email address.')]


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please enter a username for your profile!")])
    email = StringField("Email",
                        validators=[DataRequired(message='Please enter an email address to link with your profile'),
                                    Email(message="Please enter a valid email address")])
    password = PasswordField('Password', validators=[DataRequired('Please enter a strong password!')])
    repeat_password = PasswordField('Repeat Password',
                                    validators=[DataRequired('Please repeat the password'), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        self.is_not_used()
        user = db.session.query(models.User).filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please pick another username! This one is already taken :(')

    def validate_email(self, email):
        self.is_not_used()
        user = db.session.query(models.User).filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account already exists with this email id. Please enter a different one!')

    def is_not_used(self):
        # to avoid:
        #     Method 'validate_<username or email>' may be 'static'
        pass


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Please enter a username for your profile")])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField('Save Info')