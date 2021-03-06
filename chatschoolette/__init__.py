# System imports
import os
import sys

from opentok import OpenTok

# Flask imports
from flask import Flask, render_template, flash
from flask_mail import Mail
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

IMAGE_SET = UploadSet('images', IMAGES)

# Define the web app
sys.stdout.write('Creating Flask app...')
app = Flask(__name__)
sys.stdout.write('Done\n')

# Configurations for the app
sys.stdout.write('Loading config from object...')
app.config.from_object('config')
sys.stdout.write('Done\n')

# Enable CSRF Protection
sys.stdout.write('Enabling CSRF Protection...')
CsrfProtect(app)
sys.stdout.write('Done\n')

# Define the database
sys.stdout.write('Defining SQLAlchemy database...')
db = SQLAlchemy(app)
sys.stdout.write('Done\n')

# Create the login manager
sys.stdout.write('Creating login manager...')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/auth/login"
sys.stdout.write('Done\n')

# Set allowed uploads
sys.stdout.write('Configuring uploads...')
configure_uploads(app, (IMAGE_SET,))
sys.stdout.write('Done\n')

# Create OpenTok thing
sys.stdout.write('Creating OpenTok thing...')
sys.stdout.flush()
opentok = OpenTok(os.environ['OPENTOK_API_KEY'], os.environ['OPENTOK_API_SECRET'])
sys.stdout.write('Done\n')

# Register Mailer service
sys.stdout.write('Configuring Mailer service...')
mail = Mail(app)
sys.stdout.write('Done\n')

# Register error handlers
sys.stdout.write('Registering error handlers...')
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                "%s: %s" % (getattr(form, field).label.text, error),
                "alert-danger"
            )
sys.stdout.write('Done\n')

# Import all blueprints from controllers
from chatschoolette.controllers import mod_default
from chatschoolette.mod_account.controllers import mod_account
from chatschoolette.mod_admin.controllers import mod_admin
from chatschoolette.mod_auth.controllers import mod_auth
from chatschoolette.mod_chat.controllers import mod_chat

# Register blueprints
sys.stdout.write('Registering blueprint modules...')
app.register_blueprint(mod_default)
app.register_blueprint(mod_account)
app.register_blueprint(mod_admin)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_chat)
sys.stdout.write('Done\n')

sys.stdout.write('\nApp done loading.\n')
