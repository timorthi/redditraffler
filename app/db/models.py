from app.db import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    username = db.Column(db.String(64), index=True, unique=True)

    raffles = db.relationship('Raffle', backref='creator', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Raffle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    submission_id = db.Column(db.String(64), index=True, unique=True)
    submission_title = db.Column(db.String(128))
    submission_author = db.Column(db.String(64))
    subreddit = db.String(db.String(64))
    winner_count = db.Column(db.Integer)
    minimum_account_age = db.Column(db.Integer)
    minimum_ckarma = db.Column(db.Integer)
    minimum_lkarma = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return '<Raffle {}>'.format(self.submission_id)