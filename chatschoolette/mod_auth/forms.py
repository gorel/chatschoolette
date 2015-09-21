from flask.ext.uploads import (
    UploadSet,
    IMAGES,
)

from flask.ext.wtf import (
    Form,
    html5,
    RecaptchaField,
)

from flask.ext.wtf.file import (
    FileAllowed,
    FileField,
)

from wtforms import (
    BooleanField,
    PasswordField,
    RadioField,
    TextAreaField,
    TextField,
    validators,
)

IMAGE_SET = UploadSet('images', IMAGES)

class RegistrationForm(Form):
    username = TextField(
        'Username',
        validators=[
            validators.Required(
                message='You must provide a username.',
            ),
        ],
    )

    email = TextField(
        'Email',
        validators=[
            validators.Email(),
            validators.Required(
                message='You must provide your school email address.',
            ),
            validators.EqualTo(
                'confirm_email',
                message='Emails must match',
            ),
        ],
    )

    confirm_email = TextField(
        'Confirm Email',
        validators=[
            validators.Email(),
            validators.Required(
                message='Please confirm your email address.',
            ),
        ],
    )

    password = PasswordField(
        'Password',
        validators=[
            validators.Required(
                message='Please enter a password.',
            ),
            validators.EqualTo(
                'confirm_password',
                message='Passwords must match',
            ),
        ],
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            validators.Required(
                message='Please confirm your password.',
            ),
        ],
    )

    gender = RadioField(
        'Gender',
        choices=[
            ('0', 'Male'),
            ('1', 'Female'),
            ('2', 'Other'),
            ('3', 'Prefer not to answer'),
        ],
    )

    birthdate = html5.DateField(
        'Birth date',
        format='%Y-%m-%d',
    )

    profile_picture = FileField(
        'Profile Picture',
        validators=[
            FileAllowed(
                IMAGE_SET,
                'You must provide an image'
            ),
        ],
    )

    profile_description = TextAreaField(
        'Tell us about yourself!',
    )

    interests = TextAreaField(
        'List your interests, one per line!',
    )

    recaptcha = RecaptchaField()

class LoginForm(Form):
    username_or_email = TextField(
        'Username or Email',
        validators=[
            validators.Required(
                message='This field cannot be left empty.',
            ),
        ],
    )

    password = PasswordField(
        'Password',
        validators=[
            validators.Required(
                message='Please enter a password.',
            ),
        ],
    )

    remember = BooleanField(
        'Remember Me?',
    )

class ForgotForm(Form):
    email = TextField(
        'Email',
        validators=[
            validators.Email(),
            validators.Required(
                message='You must provide your school email address.',
            ),
        ],
    )
