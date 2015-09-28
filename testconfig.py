# Enable dev environment
DEBUG = True
TESTING = True
PRESERVE_CONTEXT_ON_EXCEPTION = False

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads to handle requests
THREADS_PER_PAGE = 2

# CSRF protection
CSRF_ENABLED = True
CSRF_SESSION_KEY = "abc123"
SECRET_KEY = "123abc"

# Upload configuration
UPLOADED_IMAGES_DEST = "chatschoolette/static/profile_pictures"
