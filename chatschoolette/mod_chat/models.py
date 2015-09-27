from chatschoolette import db

class ChatRoom(db.Model):
    __tablename__ = 'chatroom'
    id = db.Column(db.Integer, primary_key=True)
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

    def __repr__(self):
        return '<ChatRoom #%r>' % self.id

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
        self.timestamp = timestamp

    def __repr__(self):
        return '<ChatMessage: "%r" by %r at %r>' % (
            self.text,
            self.user.username,
            self.timestamp,
        )

class ChatQueue(db.Model):
    __tablename__ = 'chatqueue'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<ChatQueue %r>' % self.user.username
