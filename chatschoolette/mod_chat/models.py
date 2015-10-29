import datetime

from flask import (
    url_for,
)

from chatschoolette import db, opentok

class ChatRoom(db.Model):
    __tablename__ = 'chatroom'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(128))
    topic = db.Column(db.String(64))

    users = db.relationship(
        'User',
        backref='chat',
    )
    messages = db.relationship(
        'ChatMessage',
        backref='chat',
    )

    def __init__(self, topic=None):
        self.topic = topic
        self.users = []
        self.messages = []
        self.session_id = opentok.create_session().session_id

    def __repr__(self):
        return '<ChatRoom #%r>' % self.id

    def is_authorized_user(self, this_user):
        for user in self.users:
            if user.id == this_user.id:
                return True
        return False

class TextChatRoom(db.Model):
    __tablename__ = 'textchatroom'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(128))
    users = db.relationship(
        'User',
        backref='textchat',
    )
    messages = db.relationship(
        'TextChatMessage',
        backref='textchat',
    )

    def __init__(self):
        self.users = []
        self.messages = []
        self.session_id = opentok.create_session().session_id

    def __repr__(self):
        return '<TextChatRoom #%r>' % self.id

    def is_authorized_user(self, this_user):
        for user in self.users:
            if user.id == this_user.id:
                return True
        return False

class ChatMessage(db.Model):
    __tablename__ = 'chatmessage'
    id = db.Column(db.Integer, primary_key=True)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    text = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)

    def __init__(self, chatroom_id, user_id, text, timestamp):
        self.chatroom_id = chatroom_id
        self.user_id = user_id
        self.text = text
        self.timestamp = datetime.datetime(1995, 12, 25, 6, 30)

    def __repr__(self):
        return '<ChatMessage: "%r" by %r at %r>' % (
            self.text,
            self.user.username,
            self.timestamp,
        )

    @property
    def ftime(self):
        return self.timestamp.strftime('%Y-%m-%d at %I:%M %p')

class TextChatMessage(db.Model):
    __tablename__ = 'textchatmessage'
    id = db.Column(db.Integer, primary_key=True)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('textchatroom.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    text = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)

    def __init__(self, chatroom_id, user_id, text, timestamp):
        self.chatroom_id = chatroom_id
        self.user_id = user_id
        self.text = text
        self.timestamp = timestamp

    def __repr__(self):
        return '<TextChatMessage: "%r" by %r at %r>' % (
            self.text,
            self.user.username,
            self.timestamp,
        )

    @property
    def ftime(self):
        return self.timestamp.strftime('%Y-%m-%d at %I:%M %p')

class ChatQueue(db.Model):
    __tablename__ = 'chatqueue'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<ChatQueue %r>' % self.user.username

class PrivateChat(db.Model):
    __tablename__ = 'private_chat'
    id = db.Column(db.String(64), primary_key=True, index=True)
    messages = db.relationship(
        'PrivateMessage',
        backref='chat',
    )

    def __init__(self, room_id, users):
        self.id = room_id
        self.users = users
        self.messages = []

    def send(self, sender, receiver, message):
        self.messages.append(
            PrivateMessage(
                sender=sender,
                text=message,
            )
        )
        receiver.notify(
            text='You have a new message from {}'.format(sender.username),
            url=url_for('account.view_chat', chat_id=self.id),
        )
        db.session.commit()

    def other_user(self, this_user):
        for user in self.users:
            if user is not this_user:
                return user

    @classmethod
    def get_or_create(cls, room_id, users):
        chat = cls.query.get(room_id)
        if chat is None:
            chat = PrivateChat(
                room_id=room_id,
                users=users,
            )
            db.session.add(chat)
            db.session.commit()
        return chat


class PrivateMessage(db.Model):
    __tablename__ = 'private_message'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)
    sender = db.relationship('User')
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    private_chat = db.Column(db.Integer, db.ForeignKey('private_chat.id'))

    def __init__(self, sender, text, timestamp=None):
        self.sender = sender
        self.text = text
        self.timestamp = timestamp or datetime.datetime.now()

    @property
    def ftime(self):
        return self.timestamp.strftime('%m/%d/%Y at %I:%M %p')
