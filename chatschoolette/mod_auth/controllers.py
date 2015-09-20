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
        # TODO: Login code here
        # 1. Get form fields
        # 2. Check password
        # 3. Login
        return redirect(request.args.get('next') or url_for('default.home'))
    else:
        return render_template('auth/login.html', form=form)

@mod_auth.route('/logout/', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('default.home'))
