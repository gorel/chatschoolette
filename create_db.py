from chatschoolette import db

from chatschoolette.mod_account.models import (
    Interest,
    Profile,
)

from chatschoolette.mod_auth.models import (
    User,
    PasswordReset,
)

from chatschoolette.mod_chat.models import (
    ChatMessage,
    ChatQueue,
    ChatRoom,
    TextChatRoom,
    TextChatMessage,
    PrivateChat,
    PrivateMessage,
)

# This won't recreate the db, so safe to run again
db.create_all()
