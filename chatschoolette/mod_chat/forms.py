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

class StartChatForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
