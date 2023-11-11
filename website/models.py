from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oldWord = db.Column(db.String(150))
    word = db.Column(db.String(150))
    meaning = db.Column(db.String(150))
    pronoun = db.Column(db.String(150))
    type = db.Column(db.String(150))
    link = db.Column(db.String(150))
    count = db.Column(db.Integer, default=1)
    isUsed = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Word):
            return NotImplemented
        return self.word == o.word or self.oldWord == o.oldWord or self.oldWord == o.word

    def __hash__(self):
        return hash(self.oldWord)

    def __str__(self) -> str:
        return str([self.oldWord, self.word, self.meaning, self.pronoun, self.type, self.isUsed, self.link])

    def increaseCount(self):
        self.count += 1


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Word')
