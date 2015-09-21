from flask.ext.sqlalchemy import (
    orm,
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from chatschoolette import db, login_manager

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean)
    profile = db.relationship(
        'Profile',
        uselist=False,
        backref='user',
    )

    def __init__(self, username, email, password, is_admin=False, profile=None):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
        self.profile = profile

        # Call the method to load local variables NOT stored in the db
        self.init_on_load()

    @orm.reconstructor
    def init_on_load(self):
        # Any user that is logged in is automatically authenticated.
        self._is_authenticated = True
        self._is_active = True

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @property
    def is_active(self):
        return self._is_active

    @property
    def is_anonymous(self):
        return not self.is_authenticated()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()
