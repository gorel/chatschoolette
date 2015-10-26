import random
import string


from flask.ext.sqlalchemy import (
    orm,
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from chatschoolette import (
    db,
    login_manager,
)

from chatschoolette.mod_account.models import (
    Interest,
    Profile,
    profile_interests,
)

from chatschoolette.mod_chat.models import (
    ChatMessage,
    ChatQueue,
    PrivateChat,
)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

friends_table = db.Table(
    'friends_table',
    db.Column('friend1_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend2_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
)

private_chats_table = db.Table(
    'private_chats_table',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('private_chat_id', db.Integer, db.ForeignKey('private_chat.id'), primary_key=True),
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'))
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean)
    _is_active = db.Column(db.Boolean)
    banned = False

    activation_key = db.relationship(
        'ActivationKey',
        uselist=False,
        backref='user',
    )

    pw_reset = db.relationship(
        'PasswordReset',
        uselist=False,
        backref='user',
    )

    profile = db.relationship(
        'Profile',
        uselist=False,
        backref='user',
    )
    messages = db.relationship(
        'ChatMessage',
        backref='user',
    )
    queue_position = db.relationship(
        'ChatQueue',
        uselist=False,
        backref='user',
    )
    friends = db.relationship(
        'User',
        secondary=friends_table,
        primaryjoin=id==friends_table.c.friend1_id,
        secondaryjoin=id==friends_table.c.friend2_id,
    )
    private_chats = db.relationship(
        'PrivateChat',
        secondary=private_chats_table,
        backref='users',
    )
    notifications = db.relationship(
        'Notification',
        backref='user',
    )

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
        self.friends = []
        self.private_chats = []
        self.notifications = []
        self._is_active = False
        self.banned = False
        self.activation_key = ActivationKey()

        # Call the method to load local variables NOT stored in the db
        self.init_on_load()

    @orm.reconstructor
    def init_on_load(self):
        # Any user that is logged in is automatically authenticated.
        self._is_authenticated = True

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        db.session.delete(self.activation_key)
        self._is_active = value

    @property
    def is_anonymous(self):
        return not self.is_authenticated

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id

    def notify(self, text, url=None):
        self.notifications.append(Notification(user=self, text=text, url=url))
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username

    def send_password_reset(self):
        pw_reset = PasswordReset(
            user_id=self.id,
            key=''.join(
                random.choice(
                    string.ascii_letters + string.digits
                ) for _ in range(60)
            ),
        )
        db.session.add(pw_reset)
        db.session.commit()
        # TODO: Send email!

    def reset_password(self, new_pw):
        pw_reset = PasswordReset.query.filter_by(user_id=self.id).first()
        if pw_reset is not None:
            db.session.delete(pw_reset)
        self.password = generate_password_hash(new_pw)
        db.session.commit()

    def update_account(self, form):
        if form.password.data != '':
            self.reset_password(form.password.data)

        self.profile.gender = form.gender.data
        self.profile.body = form.profile_description.data

        # Update the user's interests
        self.profile.interests = [
            Interest.get_or_create(interest)
            for interest in form.interests
        ]

        if form.profile_picture.has_file():
            self.profile.set_profile_picture(form.profile_picture)

        db.session.commit()

    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()

class PasswordReset(db.Model):
    __tablename__ = "password_reset"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    key = db.Column(db.String(64), index=True)

    def __init__(self, user_id, key):
        self.user_id = user_id
        self.key = key

    def __repr__(self):
        return '<PasswordReset for %r>' % self.user.username

class ActivationKey(db.Model):
    __tablename__ = "activation_key"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    key = db.Column(db.String(64), index=True)

    def __init__(self):
        self.key = ''.join(
            random.choice(
                string.ascii_letters + string.digits
            ) for _ in range(60)
        )

    def __repr__(self):
        return '<ActivationKey for %r>' % self.user.username

class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    text = db.Column(db.String(256))
    url = db.Column(db.String(128))

    def __init__(self, user, text, url=None):
        self.user = user
        self.text = text
        self.url = url

    def __repr__(self):
        return '<Notification: %r>' % self.text

