from xmlrpc.client import Boolean
from flask_bcrypt import Bcrypt

BCRYPT = Bcrypt()

from flask import current_app


def check_email(email: str) -> Boolean:
    con = current_app.get_connection()

    if con.get_email(email) is None:
        return True
    return False


def hash_password(password: str):
    hashed_password = BCRYPT.generate_password_hash(password).decode('utf-8')

    return hashed_password


def check_user(email, password) -> Boolean:
    con = current_app.get_connection()

    if BCRYPT.check_password_hash(con.get_password(email), password):
        return True
    return False
