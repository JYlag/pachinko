from app import db
from hashutils import make_pw_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    pw_hash = db.Column(db.String(120))
    scores = db.relationship('Score', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)

    def __repr__(self):
        return '<User %r' % self.username

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, score, owner):
        self.score = score
        self.owner = owner

    def __repr__(self):
        return '<Score %r' % self.score