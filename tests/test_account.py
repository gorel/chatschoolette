from datetime import datetime
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


class AccountTestCase(unittest.TestCase):
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
        db.session.add(Interest('testing'))
        i1 = Interest('pickles')
        i2 = Interest('ketchup')
        user = User('a', 'a@a.com', 'a')
        profile = Profile(
            user,
            'a.com',
            0,
            datetime(1993, 12, 20),
            'body text',
            [i1, i2],
        )

        db.session.add(i1)
        db.session.add(i2)
        db.session.add(user)
        db.session.add(profile)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testTrue(self):
        assert True

    def test_create_interest(self):
        interest = Interest('pickles2')
        db.session.add(interest)
        db.session.commit()

        retrieve = Interest.query.filter_by(name='pickles').first()
        assert retrieve is not None
        db.session.delete(interest)
        db.session.commit()

    def test_unknown_interest(self):
        interest = Interest.query.filter_by(name='packles').first()
        assert interest is None

    def test_get_interest(self):
        interest = Interest('pickles3')
        db.session.add(interest)
        db.session.commit()

        retrieve = Interest.query.get(interest.id)
        assert retrieve is not None
        db.session.delete(interest)
        db.session.commit()

    def test_existing_interest(self):
        interest = Interest.query.filter_by(name='testing').first()
        assert interest is not None

    def test_compare_interest_less_than(self):
        i1 = Interest('a')
        i2 = Interest('b')
        i3 = Interest('c')
        assert i1 < i2

    def test_compare_interest_greater_than(self):
        i1 = Interest('a')
        i2 = Interest('b')
        i3 = Interest('c')
        assert i2 > i1

    def test_compare_interest_equal(self):
        i1 = Interest('a')
        i2 = Interest('b')
        i3 = Interest('c')
        assert i3 == i3

    def test_get_profile(self):
        profile = Profile.query.filter_by(domain='a.com').first()
        assert profile is not None

    def test_get_missing_profile(self):
        profile = Profile.query.filter_by(domain='.com').first()
        assert profile is None

    def test_load_body_text(self):
        profile = Profile.query.first()
        assert 'body text' in profile.body

    def test_get_user_from_profile(self):
        profile = Profile.query.first()
        assert profile.user is not None

    def test_get_profile_from_user(self):
        user = User.query.first()
        assert user.profile is not None

    def test_set_profile_picture(self):
        profile = Profile.query.first()
        # Actually, we need real form data to call "save" method
        # Any way to mock this properly?
        profile.has_profile_picture = True
        db.session.commit()
        # Then remove saved file from directory
        assert profile.has_profile_picture
        # Additional cleanup

    def test_repr(self):
        profile = Profile.query.first()
        expected = '<Profile %r>' % profile.user.username
        assert repr(profile) == expected
