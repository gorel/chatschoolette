from flask_login import (
    current_user,
)

from sqlalchemy import (
    or_,
)

from flask_wtf import (
    Form,
)

from flask.ext.wtf.file import (
    FileAllowed,
    FileField,
)

from wtforms import (
    PasswordField,
    RadioField,
    TextAreaField,
    TextField,
    validators,
)

from chatschoolette import (
    IMAGE_SET,
)

from chatschoolette.mod_account.models import (
    Interest,
    Profile,
)

from chatschoolette.mod_auth.models import (
    User,
)

from chatschoolette.mod_chat.models import (
    PrivateChat,
)

class EditAccountForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.interests = []

    def validate(self):
        if not Form.validate(self):
            return False

        self.interests = [
            interest.lower()
            for interest in filter(None, self.interests_text.data.splitlines())
        ]

        return True

    password = PasswordField(
        'New Password',
        validators=[
            validators.EqualTo(
                'confirm_password',
                message='Passwords must match',
            ),
        ],
    )

    confirm_password = PasswordField('Confirm New Password')

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


class SearchForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.users = []

    def validate(self):
        res = True
        if not Form.validate(self):
            res = False

        query = User.query.join(Profile)
        query = query.filter(User.id != current_user.id)
        query = query.filter(Profile.domain == current_user.profile.domain)

        if self.username.data.strip() != '':
            query = query.filter(User.username == self.username.data.strip())

        if self.email.data.strip() != '':
            query = query.filter(User.email == self.email.data.strip())

        if self.gender.data != 3:
            query = query.filter(Profile.gender == self.gender.data)

        interests = filter(None, self.interests_text.data.splitlines())
        if len(interests) > 0:
            query = query.join(Interest, Profile.interests).filter(
                or_(
                    Interest.name == interest
                    for interest in interests
                )
            )

        self.users = query.all()
        return res

    username = TextField('Username')

    email = TextField('Email')

    interests_text = TextAreaField('Interests (one per line)')

    gender = RadioField(
        'Gender',
        choices=[
            (0, 'Male'),
            (1, 'Female'),
            (2, 'Other'),
            (3, 'Any'),
        ],
        default=3,
        coerce=int,
    )

class SendMessageForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.chat = None
        self.message = None

    def validate(self):
        res = True
        if not Form.validate(self):
            res = False

        self.message = self.message_text.data
        return res

    message_text = TextAreaField("What's on your mind?")
