from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)

from flask.ext.login import (
    current_user,
    login_required,
)

# Import main DB and Login Manager for app
from chatschoolette import db, login_manager

# Import forms
from chatschoolette.mod_chat.forms import (
    StartChatForm,
)

# Create a blueprint for this module
mod_chat = Blueprint('chat', __name__, url_prefix='/chat')

# Set all routing for the module
@mod_chat.route('/<chat_id>', methods=['GET', 'POST'])
@login_required
def chat(chat_id=None):
    form = StartChatForm(request.form)
    if chat_id is not None and chat_id.isdigit():
        # Make sure user is authorized to be in this chat
        chatroom = ChatRoom.get(int(chat_id))
        if chatroom and chatroom.is_authorized_user(current_user):
            # Remove the user from the queue
            db.session.delete(current_user.queue_position)
            db.session.commit()
            return render_template('chat/chat.html')
        else:
            return render_template('chat/home.html', form=form)

    # The user is loading the chat select screen and doesn't have a match yet
    if form.validate_on_submit():
        # TODO: Check the settings the user set for their chat preferences
        # Let the user wait somewhere?
        pass
    else:
        return render_template('chat/home.html', form=form)
