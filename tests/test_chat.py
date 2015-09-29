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

class ChatTestCase(unittest.TestCase):
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testTrue(self):
        return True

    # TODO: Write more tests!
