import datetime
import os

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
from chatschoolette import db, login_manager, flash_form_errors, opentok

# Import forms
from chatschoolette.mod_chat.forms import (
    StartChatForm,
)

from chatschoolette.mod_chat.models import (
    ChatMessage,
    ChatRoom,
    TextChatMessage,
    TextChatRoom,
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
    form.domain.data = current_user.profile.domain
    # The user is loading the chat select screen and doesn't have a match yet
    if form.validate_on_submit():
        if form.is_video:
            if form.is_new:
                db.session.add(form.room)
            form.room.users.append(current_user)
            db.session.commit()
            return redirect(url_for('chat.video_chat', room_id=form.room.id))
        else:
            if form.is_new:
                db.session.add(form.room)
            form.room.users.append(current_user)
            db.session.commit()
            return redirect(url_for('chat.text_chat', room_id=form.room.id))
    else:
        flash_form_errors(form)
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

@mod_chat.route('/video_chat/<int:room_id>', methods=['GET'])
@mod_chat.route('/video_chat/<int:room_id>/', methods=['GET'])
@login_required
def video_chat(room_id):
    # Make sure user is authorized to be in this chat
    chatroom = ChatRoom.query.get(room_id)

    if not chatroom:
        flash(
            "Oops! Looks like you don't belong in that chat room!",
            "alert-warning",
        )
        return redirect(url_for('chat.home'))

    token = opentok.generate_token(str(chatroom.session_id))
    return render_template(
        'chat/video.html',
        session_id=chatroom.session_id,
        room_id=room_id,
        token=token,
        api_key=os.environ['OPENTOK_API_KEY'],
    )

@mod_chat.route('/text_chat/<int:room_id>', methods=['GET'])
@mod_chat.route('/text_chat/<int:room_id>/', methods=['GET'])
@login_required
def text_chat(room_id):
    # Make sure user is authorized to be in this chat
    chatroom = TextChatRoom.query.get(room_id)

    if not chatroom or not chatroom.is_authorized_user(current_user):
        flash(
            "Oops! Looks like you don't belong in that chat room!",
            "alert-warning",
        )
        return redirect(url_for('chat.home'))

    token = opentok.generate_token(str(chatroom.session_id))
    return render_template(
        'chat/text.html',
        session_id=chatroom.session_id,
        room_id=room_id,
        token=token,
        api_key=os.environ['OPENTOK_API_KEY'],
    )

@mod_chat.route('/record', methods=['POST'])
@mod_chat.route('/record/', methods=['POST'])
def record():
    msg = request.form['message']
    current_user.messages.append(
        ChatMessage(
            chatroom_id=current_user.chat.id,
            user_id=current_user.id,
            text=msg,
            timestamp=datetime.datetime.now(),
        )
    )
    db.session.commit()
    return redirect(url_for('default.home'))
