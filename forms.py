from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message='Please enter your name')])
    email = StringField("Email", validators=[DataRequired('Please enter your email'), Email(message="Not a valid "
                                                                                                    "email address")])
    subject = StringField("Subject")
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=4, message="Your message is too short")])
    # recaptcha = RecaptchaField()
    submit = SubmitField("Send")
# [DataRequired(), Email(message='Not a valid email address.')]
