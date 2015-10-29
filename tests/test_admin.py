import os
import unittest

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
)
from flask.ext.uploads import (
    configure_uploads,
    IMAGES,
    UploadSet,
)
from flask.ext.wtf import (
    CsrfProtect,
)

from chatschoolette import app, db

from chatschoolette.mod_account.models import (
    Interest,
    Profile,
)

from chatschoolette.mod_auth.models import (
    User,
)

from chatschoolette.mod_chat.models import (
    ChatMessage,
    ChatQueue,
    ChatRoom,
)

from config import BASE_DIR


class AdmniTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        )
        self.app = app
        self.client = app.test_client()
        db.create_all()
        
        admin = User(
            username='admin',
            email='admin@test.com',
            password='admin',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

        user = User(
            username='user',
            email='user@test.com',
            password='user'
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testTrue(self):
        return True

    def test_is_admin(self):
        username = 'admin'
        user = User.query.filter_by(username=username).first()
        assert user.is_admin is True

    def test_is_not_admin(self):
        username = 'user'
        user = User.query.filter_by(username=username).first()
        assert user.is_admin is False

    def test_ban_user(self):
        username = 'user'
        user = User.query.filter_by(username=username).first()
        assert user.banned is False

        user.banned = True
        assert user.banned is True
