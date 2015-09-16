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
#from chatschoolette.mod_auth.forms import (
#)

# Import models
#from chatschoolette.mod_auth.models import (
#)

# Create a blueprint for this module
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set all routing for the module
@mod_auth.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    else:
        # TODO: Register the new user and log them in
        return redirect(request.args.get('next') or url_for('/'))

@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        # TODO: Login code here
        # 1. Get form fields
        # 2. Check password
        # 3. Login
        return redirect(request.args.get('next') or  url_for('/'))

@mod_auth.route('/logout/', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))
