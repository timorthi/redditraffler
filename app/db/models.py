from app.extensions import db
from datetime import datetime
from sqlalchemy import inspect
from flask import current_app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    username = db.Column(db.Text, index=True, unique=True)

    raffles = db.relationship("Raffle", backref="creator", lazy=True)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Raffle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    submission_id = db.Column(db.Text, index=True, unique=True)
    submission_title = db.Column(db.Text)
    submission_author = db.Column(db.Text)
    subreddit = db.Column(db.Text)
    winner_count = db.Column(db.Integer)
    min_account_age = db.Column(db.Integer)
    min_comment_karma = db.Column(db.Integer)
    min_link_karma = db.Column(db.Integer)
    ignored_users = db.Column(db.Text, nullable=True)

    winners = db.relationship(
        "Winner", backref="raffle", lazy=True, cascade="all, delete-orphan"
    )

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, index=True)

    def __repr__(self):
        return "<Raffle {}>".format(self.submission_id)

    def is_verified(self):
        return self.creator and (self.submission_author == self.creator.username)

    def created_at_readable(self):
        return (
            self.created_at.strftime("%B %-d %Y, %-I:%M%p")
            .replace("AM", "am")
            .replace("PM", "pm")
        )

    def as_dict(self):
        exclude = set(["id", "updated_at"])
        res = {}
        for col in inspect(self).mapper.column_attrs:
            if col.key == "created_at":
                res[col.key] = getattr(self, col.key).timestamp()
            elif col.key not in exclude:
                res[col.key] = getattr(self, col.key)
        res["created_at_readable"] = self.created_at_readable()
        return res

    def ignored_users_list(self):
        return self.ignored_users.split(",")


class Winner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    username = db.Column(db.Text)
    account_age = db.Column(db.Integer)
    comment_karma = db.Column(db.Integer)
    link_karma = db.Column(db.Integer)
    comment_url = db.Column(db.Text)

    raffle_id = db.Column(
        db.Integer, db.ForeignKey("raffle.id"), nullable=False, index=True
    )
