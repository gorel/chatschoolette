from flask import (
    Blueprint,
    flash,
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
from chatschoolette import db, login_manager, flash_form_errors

# Import forms
from chatschoolette.mod_auth.forms import (
    ActivateAccountForm,
    LoginForm,
    RegistrationForm,
)

# Import models
from chatschoolette.mod_account.models import (
    Interest,
    Profile,
    profile_interests,
)

from chatschoolette.mod_auth.models import (
    User,
)

# Create a blueprint for this module
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set all routing for the module
@mod_auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create the user account by first
        db.session.add(form.user)
        db.session.add(form.profile)
        db.session.commit()

        # Add the user's profile picture if they provided one
        if form.profile_picture.has_file():
            form.profile.set_profile_picture(form.profile_picture)

        # Finally, commit the db session
        db.session.commit()

        # Log the user in and redirect to the homepage
        login_user(form.user, remember=form.remember.data, force=True)
        flash('Your account has been created.', 'alert-success')
        return redirect(request.args.get('next') or url_for('default.home'))
    else:
        flash_form_errors(form)
        return render_template('auth/register.html', form=form)

@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # User has authenticated. Log in.
        flash('Welcome back to ChatSchoolette!', 'alert-success')
        login_user(form.user, remember=form.remember.data, force=True)
        return redirect(request.args.get('next') or url_for('default.home'))
    else:
        flash_form_errors(form)
        return render_template('auth/login.html', form=form)

@mod_auth.route('/logout/', methods=['POST'])
def logout():
    # Don't set login required, because it will send the user to the login page
    # before redirecting them to logout. It doesn't make much sense to the user.
    if current_user.is_authenticated:
        logout_user()
    flash('You have successfully logged out.', 'alert-success')
    return redirect(url_for('default.home'))

@mod_auth.route('/reset/<key>', methods=['GET', 'POST'])
def reset(key):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        form.user.reset_password(form.password.data)
        flash(
            "Your password has been successfully reset!",
            "alert-success",
        )
        login_user(form.user, force=True)
        return redirect(url_for('default.home'))
    else:
        flash_form_errors(form)
        form.reset_key.data = key
        return render_template('auth/reset.html', form=form)

@mod_auth.route('/activate/<key>', methods=['GET', 'POST'])
def activate(key):
    form = ActivateAccountForm()
    if form.validate_on_submit():
        form.user.set_active()
        db.session.commit()
        flash('Your account is now activated! Get chatting!', 'alert-success')
        return redirect(url_for('default.home'))
    else:
        flash_form_errors(form)
        form.activation_key.data = key
        return render_template('auth/activate.html', form=form)
