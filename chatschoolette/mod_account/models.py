import functools

from chatschoolette import (
    app,
    db,
)

profile_interests = db.Table(
    'profile_interests',
    db.Column('profile_id', db.Integer, db.ForeignKey('profile.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id')),
)

@functools.total_ordering
class Interest(db.Model):
    __tablename__ = 'interest'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Interest %r>' % self.name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    @classmethod
    def get_or_create(cls, name):
        interest = cls.query.filter_by(name=name).first()
        if interest is None:
            interest = Interest(name=name)
            db.session.add(interest)
            db.session.commit()
        return interest

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Location is deterministic; just store whether or not the user has a pic
    has_profile_picture = db.Column(db.Boolean)

    # Demographic information
    domain = db.Column(db.String(64), index=True)
    gender = db.Column(db.Integer)
    birthdate = db.Column(db.DateTime)

    # Profile information
    body = db.Column(db.Text)
    interests = db.relationship(
        'Interest',
        secondary=profile_interests,
        backref='profiles',
    )

    def __init__(
        self,
        user,
        domain,
        gender,
        birthdate,
        body,
        interests=[],
    ):
        self.user = user
        self.domain = domain
        self.gender = gender
        self.birthdate = birthdate
        self.body = body
        self.interests = interests
        self.has_profile_picture = False

    def __repr__(self):
        return '<Profile %r>' % self.user.username

    def set_profile_picture(self, picture):
        picture.data.save(
            "{directory}/{username}".format(
                directory=app.config['UPLOADED_IMAGES_DEST'],
                username=self.user.username,
            ),
        )
        self.has_profile_picture = True
        db.session.commit()
