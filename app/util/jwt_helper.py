from flask import current_app
import jwt


ALGORITHM = "HS256"


def encode(payload):
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm=ALGORITHM)


def decode(token):
    return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[ALGORITHM])
