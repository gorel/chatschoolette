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

from chatschoolette.mod_account.models import (
    Profile,
)

# Import main DB and Login Manager for app
from chatschoolette import db, login_manager, flash_form_errors

# Import forms
from chatschoolette.mod_account.forms import (
    EditAccountForm,
    SearchForm,
    SendMessageForm,
)

from chatschoolette.mod_chat.models import (
    PrivateChat,
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
    id1 = min(current_user.id, profile.user.id)
    id2 = max(current_user.id, profile.user.id)
    chat_id = '{}-{}'.format(id1, id2)
    if profile is None:
        flash(
            "No user with that profile ID was found!",
            "alert-warning",
        )
        return render_template('account/404.html'), 404
    return render_template('account/view.html', profile=profile, chat_id=chat_id)

@mod_account.route('/friend/<int:profile_id>', methods=['POST'])
@mod_account.route('/friend/<int:profile_id>/', methods=['POST'])
@login_required
def friend(profile_id):
    profile = Profile.query.get(profile_id)
    if profile is None:
        flash("No user found", "alert-warning")
    else:
        user = profile.user
        current_user.friends.append(user)
        db.session.commit()
        flash('You are now friends with {}!'.format(user.username), 'alert-success')
    return redirect(url_for('account.friends_list'))

@mod_account.route('/unfriend/<int:profile_id>', methods=['POST'])
@mod_account.route('/unfriend/<int:profile_id>/', methods=['POST'])
@login_required
def unfriend(profile_id):
    profile = Profile.query.get(profile_id)
    if profile is None:
        flash("No user found", "alert-warning")
    else:
        user = profile.user
        if user in current_user.friends:
            current_user.friends.remove(user)
            db.session.commit()
            flash('You are no longer friends with {}'.format(user.username), 'alert-danger')
    return redirect(url_for('account.friends_list'))

@mod_account.route('/friends', methods=['GET'])
@mod_account.route('/friends/', methods=['GET'])
@login_required
def friends_list():
    return render_template('account/friendslist.html')

@mod_account.route('/view_chat/<chat_id>', methods=['GET', 'POST'])
@mod_account.route('/view_chat/<chat_id>/', methods=['GET', 'POST'])
@login_required
def view_chat(chat_id):
    users = [User.query.get(int(id)) for id in chat_id.split('-')]
    chat = PrivateChat.get_or_create(chat_id, users)
    other_user = [u for u in users if u.id != current_user.id][0]

    form = SendMessageForm()
    if form.validate_on_submit():
        chat.send(current_user, other_user, form.message)
        return redirect(url_for('account.view_chat', chat_id=chat_id))
    else:
        return render_template('account/view_chat.html', form=form, other_user=other_user, chat=chat)
