from datetime import datetime

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
    HiddenField,
    PasswordField,
    RadioField,
    TextAreaField,
    TextField,
    validators,
)

from chatschoolette.mod_account.models import (
    Interest,
    Profile,
)

from chatschoolette.mod_auth.models import (
    User,
    PasswordReset,
)

from chatschoolette import (
    IMAGE_SET,
)

class RegistrationForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None
        self.profile = None
        self.interests = None

    def validate(self):
        if not Form.validate(self):
            return False

        # First check if the user has already created an account
        user = User.get_by_email(self.email.data)
        if user and user.check_password(self.password.data):
            self.user = user
            return True

        if self.gender.data not in range(0, 4):
            self.gender.errors.append('Please select a valid gender.')
            return False

        if ((datetime.now().date() - self.birthdate.data).days / 365) < 18:
            self.birthdate.errors.append(
                'Sorry, you must be 18 or older to use ChatSchoolette :(',
            )
            return False

        if User.get_by_username(self.username.data):
            self.username.errors.append(
                'Sorry, that username is already taken.',
            )
            return False

        if User.get_by_email(self.email.data):
            self.email.errors.append(
                'It looks like that email address is already registered!',
            )
            return False

        # Add each of the user's interests
        self.interests = filter(None, self.interests_text.data.splitlines())
        self.interests = [s.lower() for s in self.interests]
        self.interests = [
            Interest.get_or_create(interest)
            for interest in self.interests
        ]

        # Create a new user
        self.user = User(
            username=self.username.data,
            email=self.email.data,
            password=self.password.data,
        )

        # Create a new user profile
        self.profile = Profile(
            user=self.user,
            domain=self.email.data.split('@')[1],
            gender=self.gender.data,
            birthdate=self.birthdate.data,
            body=self.profile_description.data,
            interests=self.interests,
        )

        return True

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
            (0, 'Male'),
            (1, 'Female'),
            (2, 'Other'),
            (3, 'Prefer not to answer'),
        ],
        coerce=int,
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

    interests_text = TextAreaField(
        'List your interests, one per line!',
    )

    remember = BooleanField(
        'Remember Me?',
    )

    recaptcha = BooleanField('Testing')#RecaptchaField()

class LoginForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(
            username=self.username_or_email.data
        ).first()
        if user is None:
            user = User.query.filter_by(
                email=self.username_or_email.data
            ).first()

        if user is None:
            self.username_or_email.errors.append(
                "No account with that username or email found!"
            )
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append(
                "Incorrect password!"
            )
            return False

        if user.banned:
            self.username_or_email.errors.append(
                "Your account has been banned because you are a horrible person! "
                "Maybe you should think about this in the future."
            )
            return False

        self.user = user
        return True

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
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False

        self.user = User.query.filter_by(email=self.email.data).first()
        return self.user is not None

    email = TextField(
        'Email',
        validators=[
            validators.Email(),
            validators.Required(
                message='You must provide your school email address.',
            ),
        ],
    )

class ResetPasswordForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False

        pw = PasswordReset.query.filter_by(key=self.key.data).first()
        if not pw:
            self.password.errors.append('Bad password reset key')
            return False

        self.user = pw.user
        return True

    password = PasswordField(
        'New Password',
        validators=[
            validators.Required(
                message='Please enter a new password.',
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

    key = HiddenField()


class ActivateAccountForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(activation_key=self.activation_key).first()
        if user is None:
            return False

        self.user = user
        return True

    activate_key = HiddenField()
