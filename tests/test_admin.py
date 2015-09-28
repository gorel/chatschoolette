import os

from flask import Flask
from flask.ext.testing import TestCase
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

from chatschoolette import db

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


class AdmniTestCase(TestCase):

    def create_app(self):
        # Define the web app
        app = Flask(__name__)

        # Enable CSRF Protection
        csrf = CsrfProtect()
        csrf.init_app(app)

        # Configurations for the app
        app.config.from_object('testconfig')

        # Define the database
        db = SQLAlchemy(app)

        # Create the login manager
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = "/auth/login"

        # Set allowed uploads
        IMAGE_SET = UploadSet('images', IMAGES)
        configure_uploads(app, (IMAGE_SET,))

        # Register error handlers
        @app.errorhandler(404)
        def not_found(error):
            return render_template('404.html'), 404

        # Import all blueprints from controllers
        from chatschoolette.controllers import mod_default
        from chatschoolette.mod_account.controllers import mod_account
        from chatschoolette.mod_admin.controllers import mod_admin
        from chatschoolette.mod_auth.controllers import mod_auth
        from chatschoolette.mod_chat.controllers import mod_chat

        # Register blueprints
        app.register_blueprint(mod_default)
        app.register_blueprint(mod_account)
        app.register_blueprint(mod_admin)
        app.register_blueprint(mod_auth)
        app.register_blueprint(mod_chat)

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testTrue(self):
        return True
