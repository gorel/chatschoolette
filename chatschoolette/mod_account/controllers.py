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

from chatschoolette.mod_account.models import (
    Profile,
)

# Import main DB and Login Manager for app
from chatschoolette import db, login_manager, flash_form_errors

# Import forms
from chatschoolette.mod_account.forms import (
    EditAccountForm,
    SearchForm,
)

# Create a blueprint for this module
mod_account = Blueprint('account', __name__, url_prefix='/account')

# Set all routing for the module
@mod_account.route('/home/', methods=['GET'])
@login_required
def home():
    return render_template('account/home.html')

@mod_account.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditAccountForm()
    if form.validate_on_submit():
        current_user.update_account(form)
        flash(
            "Your account has been updated successfully.",
            "alert-success",
        )
        return redirect(url_for('account.home'))
    else:
        flash_form_errors(form)
        form.gender.data = current_user.profile.gender
        form.profile_description.data = current_user.profile.body
        form.interests_text.data = '\n'.join(
            interest.name for interest in current_user.profile.interests
        )
        return render_template('account/edit.html', form=form)

@mod_account.route('/search/', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        if len(form.users) == 0:
            flash(
                "Oops! No results! Maybe you shouldn't be so picky :)",
                "alert-warning",
            )
            return render_template('account/search.html', form=form)
        return render_template('account/search_results.html', users=form.users)
    else:
        flash_form_errors(form)
        return render_template('account/search.html', form=form)

@mod_account.route('/<int:profile_id>/', methods=['GET'])
def view(profile_id):
    profile = Profile.query.get(profile_id)
    if profile is None:
        flash(
            "No user with that profile ID was found!",
            "alert-warning",
        )
        return render_template('account/404.html'), 404
    return render_template('account/view.html', profile=profile)
