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
    SubmitField,
    TextAreaField,
    TextField,
    validators,
)

from chatschoolette.mod_auth.models import (
    User,
    Profile,
)

from chatschoolette.mod_chat.models import (
    ChatRoom,
)

class StartChatForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.room = None
        self.is_new = False
        self.is_video = False

    def validate(self):
        if not Form.validate(self):
            return False

        if self.video_button.data:
            self.is_video = True
            for room in ChatRoom.query.join(User, ChatRoom.users).join(Profile, User.profile).filter(
                Profile.domain == self.domain.data
            ):
                if len(room.users) == 1:
                    self.room = room
            if not self.room:
                self.is_new = True
                self.room = ChatRoom()
        else:
            # Do all of Stephen's witchcraft and sorcery here
            pass

        return True

    video_button = SubmitField('Video')
    text_button = SubmitField('Text')
    domain = HiddenField()
