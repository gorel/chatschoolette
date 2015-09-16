# System imports
import sys

# Flask imports
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
)

# Define the web app
sys.stdout.write('Creating Flask app...')
app = Flask(__name__)
sys.stdout.write('Done\n')

# Configurations for the app
sys.stdout.write('Loading config from object...')
app.config.from_object('config')
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

# Register error handlers
sys.stdout.write('Registering error handlers...')
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
sys.stdout.write('Done\n')

# Import all blueprints from controllers
from chatschoolette.mod_account.controllers import mod_account
from chatschoolette.mod_admin.controllers import mod_admin
from chatschoolette.mod_auth.controllers import mod_auth
from chatschoolette.mod_chat.controllers import mod_chat

# Register blueprints
sys.stdout.write('Registering blueprint modules...')
app.register_blueprint(mod_account)
app.register_blueprint(mod_admin)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_chat)
sys.stdout.write('Done\n')

# Import base controller
import chatschoolette.controllers

# Build database with SQLAlchemy
sys.stdout.write('Building database with SQLAlchemy...')
db.create_all()
sys.stdout.write('Done\n')

sys.stdout.write('\nApp done loading.\n')
