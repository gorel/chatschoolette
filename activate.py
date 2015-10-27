from chatschoolette import db
from chatschoolette.mod_auth.models import User

for user in User.query.all():
    print(user)
    user.is_active = True
    print('User {} now active.'.format(user.username))
db.session.commit()
print('Done')
