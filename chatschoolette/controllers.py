from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from werkzeug import (
    check_password_hash,
    generate_password_hash
)

# Create the default module blueprint
mod_default = Blueprint('default', __name__)

# Set all routing for the default app (not within modules)
@mod_default.route('/')
@mod_default.route('/home')
@mod_default.route('/index.html')
def home():
    return render_template('index.html')

@mod_default.route('/about/')
def about():
    return render_template('about.html')
