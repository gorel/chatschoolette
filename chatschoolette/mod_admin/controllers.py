from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask.ext.login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from chatschoolette.mod_auth.models import (
    User,
)

# Import main DB and Login Mangaer for app
from chatschoolette import db, login_manager

# Create a blueprint for this module
mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

# Set all routing for the module
@mod_admin.route('/home/', methods=['GET'])
@login_required
def home():
    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to view that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))
    users = User.query.filter(User.id != current_user.id)
    return render_template('admin/home.html', users=users)

@mod_admin.route('/ban/<int:user_id>/', methods=['POST'])
@login_required
def ban(user_id):
    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to view that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))
    user = User.query.get(user_id)
    if user is None:
        flash(
            "No user with that user_id found!",
            "alert-warning",
        )
    else:
        flash(
            "User %s has been banned." % user.username,
            "alert-success",
        )
        user.messages = []
        db.session.delete(user.queue_position)
        db.session.delete(user.pw_reset)
        db.session.delete(user.profile)
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('admin.home'))

@mod_admin.route('/reset_password/<int:user_id>/', methods=['POST'])
@login_required
def reset_password(user_id):
    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to view that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))
    user = User.query.get(user_id)
    if user is None:
        flash(
            "No user with that user_id found!",
            "alert-warning",
        )
    else:
        user.send_password_reset_link()
        flash(
            "Password reset link sent to user %r" % user.username,
            "alert-success",
        )

    return redirect(url_for('admin.home'))
