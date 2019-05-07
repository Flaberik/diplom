from app import db, lm
from flask_login import UserMixin

ROLE_USER = 0
ROLE_ADMIN = 1


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.login)

    @lm.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return "'id': %r, 'teacher_name': %r" % (self.id, self.teacher_name)
        #return '<Teacher %r>' % (self.teacher_name)


class Lessons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return "'id': %r, 'lesson_name': %r" % (self.id, self.lesson_name)
        #return '<Lesson %r>' % (self.lesson_name)


class Groups(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return "'id': %r, 'group_name': %r" % (self.id, self.group_name)
        #return '<Group %r>' % (self.group_name)

    def serialize(self, whatTo):
        result = {}
        if 'id' in whatTo:
            result['id'] = self.id
        if 'group_name' in whatTo:
            result['date'] = str(self.group_name)
        return result

    def as_dict(self):
       return {c.group_name: getattr(self, c.group_name) for c in self.__table__.columns}


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, index=True)
    lesson_id = db.Column(db.Integer, index=True)
    teacher_id = db.Column(db.Integer, index=True)
    day_week = db.Column(db.String(2), index=True)
    pair = db.Column(db.String(1), index=True)
    num_room = db.Column(db.String(4), index=True)
    denom = db.Column(db.String(1), index=True)
    hash_sum = db.Column(db.String(128), index=True, unique=True)

    def __json__(self):
        return ['id', 'group_id', 'lesson_id', 'teacher_id']
    def __repr__(self):
        #return '<Schedule %r>' % (self.id)
        return "'id': %a, 'group_id': %a, 'lesson_id': %a, 'teacher_id': %a, 'day_week': %a, 'pair': %a, 'num_room': %a, 'denom': %a" % (self.id, self.group_id, self.lesson_id, self.teacher_id, self.day_week, self.pair, self.num_room, self.denom)
