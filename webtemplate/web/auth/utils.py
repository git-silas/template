from flask_bcrypt import Bcrypt

BCRYPT = Bcrypt()

from flask import current_app


def check_email(email: str):
    con = current_app.get_connection()

    print(con.get_email(email))

    if con.get_email(email) is None:
        return True
    return False


def hash_password(password: str):
    hashed_password = BCRYPT.generate_password_hash(password).decode('utf-8')

    return hashed_password
