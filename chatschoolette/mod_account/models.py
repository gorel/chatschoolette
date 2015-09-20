from chatschoolette import db

profile_interests = db.Table(
    'profile_interests',
    db.Column('profile_id', db.Integer, db.ForeignKey('profile.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id')),
)

class Interest(db.Model):
    __tablename__ = 'interest'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Interest %r>' % self.name

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Location is deterministic; just store whether or not the user has a pic
    profile_pic = db.Column(db.Boolean)

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

    def __init__(self, profile_pic, domain, gender, birthdate, body, interests):
        self.profile_pic = profile_pic
        self.domain = domain
        self.gender = gender
        self.birthdate = birthdate
        self.body = body
        self.interests = interests

    def __repr__(self):
        return '<Profile %r>' % self.user
