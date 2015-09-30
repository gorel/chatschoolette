from datetime import datetime
import os
import unittest

from flask import Flask, escape
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

class AuthTestCase(unittest.TestCase):
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

        user = User(
            username='test_default',
            email='unit_test_default@test.com',
            password='hunter2',
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testTrue(self):
        return True

    def test_account_not_exists(self):
        username = 'test_user'
        user = User.query.filter_by(username=username).first()
        assert user is None

    def test_account_exists(self):
        username = 'test_default'
        user = User.query.filter_by(username=username).first()
        assert user is not None

    def test_create_user(self):
        username = 'test_create_user'
        email = escape('unit_test_create_user@test.com')
        password = 'hunter2'

        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()

        assert user is not None

    def test_delete_user(self):
        user = User.query.first()
        username = user.username
        db.session.delete(user)
        db.session.commit()

        user = User.query.filter_by(username=username).first()
        assert user is None
