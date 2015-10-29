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
    users = User.query.all()
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
        if user.queue_position:
            db.session.delete(user.queue_position)
        if user.pw_reset:
            db.session.delete(user.pw_reset)
        user.banned = True
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
	user.send_password_reset_link()
	flash(
        "Password reset link sent to user %r" % user.username,
        "alert-success",
    )

    return redirect(url_for('admin.home'))

@mod_admin.route('/view_chat_logs/<int:user_id>', methods=['GET'])
@mod_admin.route('/view_chat_logs/<int:user_id>/', methods=['GET'])
@login_required
def view_chat_logs(user_id):
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
        return redirect(url_for('admin.home'))
    else:
        return render_template('admin/chat_logs.html', user=user)
