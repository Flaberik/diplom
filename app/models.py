from app import db, lm
from flask_login import UserMixin


ROLE_USER = 0
ROLE_ADMIN = 1

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(120), index = True, unique = True)

    def __repr__(self):
        return '<User %r>' % (self.login)

    @lm.user_loader
    def load_user(id):
        return User.query.get(int(id))

class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    teacher_name = db.Column(db.String(128), index = True, unique = True)

    def __repr__(self):
        return '<Teacher %r>' % (self.teacher_name)