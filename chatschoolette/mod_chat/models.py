from chatschoolette import db

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages = db.relationship(
        'ChatMessage',
        backref='chat',
        lazy='dynamic',
    )

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    text = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)
