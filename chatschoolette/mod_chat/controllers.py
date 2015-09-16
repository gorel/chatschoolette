from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)

from flask.ext.login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from werkzeug import (
    check_password_hash,
    generate_password_hash,
)

# Import main DB and Login Manager for app
from chatschoolette import db, login_manager

# Import forms
#from chatschoolette.mod_chat.forms import (
#)

# Import models
#from chatschoolette.mod_chat.models import (
#)

# Create a blueprint for this module
mod_chat = Blueprint('chat', __name__, url_prefix='/chat')

# Set all routing for the module
@mod_chat.route('/<chat_id>', methods=['GET', 'POST'])
def chat(chat_id=None):
    if chat_id is not None:
        # TODO: Make sure user is chatorized to be in this chat
        pass
    if request.method == 'GET':
        return render_template('chat/home.html')
    else:
        # TODO: Check the settings the user set for their chat preferences
        pass
