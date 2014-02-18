from flask.ext.login import UserMixin

from app import db, bcrypt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64))
    completed = db.Column(db.Boolean, default=False)
    order = db.Column(db.SmallInteger)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<TodoItem %r>' % (self.title)

    def serialize(self):
        return {
           'id': self.id,
           'title': self.title,
           'completed': self.completed,
           'order': self.order
       }

    