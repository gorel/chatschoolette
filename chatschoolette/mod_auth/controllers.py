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
from chatschoolette import db, login_manager

# Import forms
from chatschoolette.mod_auth.forms import (
    LoginForm,
    RegistrationForm,
)

# Import models
from chatschoolette.mod_account.models import (
    Interest,
    Profile,
)

from chatschoolette.mod_auth.models import (
    User,
)

# Create a blueprint for this module
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set all routing for the module
@mod_auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        # TODO: Lots of error checking for unique values
        # Login user if the username/email and password match existing account
        interests = []

        # Add each of the user's interests
        for interest_name in filter(None, form.interests.data.splitlines()):
            interest_name = interest_name.lower()
            interest = Interest.query.filter_by(name=interest_name).first()

            # Add a new interest to the DB if it doesn't exist
            if interest is None:
                interest = Interest(name=interest_name)
                db.session.add(interest)

            interests.append(interest)

        # Create a new user profile
        profile = Profile(
            profile_pic=(form.profile_picture.data is not None),
            domain=form.email.data.split('@')[1],
            gender=form.gender.data,
            birthdate=form.birthdate.data,
            body=form.profile_description.data,
            interests=interests,
        )
        db.session.add(profile)

        # Create a new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            profile=profile,
        )
        db.session.add(user)

        db.session.commit()

        # Log the user in and redirect to the homepage
        login_user(user)
        flash('Your account has been created.', 'alert-success')
        return redirect(request.args.get('next') or url_for('default.home'))
    else:
        # TODO: flash errors
        return render_template('auth/register.html', form=form)

@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        if '@' in form.username_or_email.data:
            user = User.get_by_email(form.username_or_email.data)
            if user is None:
                # TODO: Prepopulate email field?
                flash('No account with that email exists!', 'alert-warning')
                return redirect(url_for('auth.register'))
        else:
            user = User.get_by_username(form.username_or_email.data)
            if user is None:
                # TODO: Prepopulate user field?
                flash('No account with that username exists!', 'alert-warning')
                return redirect(url_for('auth.register'))

        if not user.check_password(form.password.data):
            flash('Incorrect password! Try again?', 'alert-danger')
            return render_template('auth/login.html', form=form)

        # User has authenticated. Log in.
        login_user(user, remember=form.remember.data)
        return redirect(request.args.get('next') or url_for('default.home'))
    else:
        return render_template('auth/login.html', form=form)

@mod_auth.route('/logout/', methods=['POST'])
def logout():
    # Don't set login required, because it will send the user to the login page
    # before redirecting them to logout. It doesn't make much sense to the user.
    if current_user.is_authenticated:
        logout_user()
    flash('You have successfully logged out.', 'alert-success')
    return redirect(url_for('default.home'))
