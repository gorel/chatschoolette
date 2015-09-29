from flask import (
    Blueprint,
    flash,
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
@mod_chat.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if not current_user.is_active:
        flash(
            'You must activate your account before you can start chatting!',
            'alert-warning',
        )
        return redirect(url_for('default.home'))

    form = StartChatForm()

    # The user is loading the chat select screen and doesn't have a match yet
    if form.validate_on_submit():
        # TODO: Check the settings the user set for their chat preferences
        # Let the user wait somewhere?
        # IDEA:
        # Set the user in a chat queue, but go ahead and put them in a room
        # Allow them to sit there and wait
        # As new users click chat, see if they match the preferences submitted
        # If so, add them to existing room
        #
        # Basically, as an algorithm:
        # for user2 in chat_queue:
        #     if user2.prefs match user1 and user1.prefs match user2:
        #         user1.join(user2.chatroom)
        #     else:
        #         user2.join(new chat room)
        #         chat_queue.add(user2)
        pass
    else:
        return render_template('chat/home.html', form=form)

@mod_chat.route('/room/<int:chat_id>', methods=['GET'])
@login_required
def room(chat_id):
    # Make sure user is authorized to be in this chat
    chatroom = ChatRoom.query.get(chat_id)

    if chatroom and chatroom.is_authorized_user(current_user):
        # Remove the user from the queue
        db.session.delete(current_user.queue_position)
        db.session.commit()
        return render_template('chat/chat.html')
    else:
        flash(
            "Oops! Looks like you don't belong in that chat room!",
            "alert-warning",
        )
        return redirect(url_for('chat.home'))
