from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    # Hash the password before storing it
    return generate_password_hash(password)


def check_password(db_password, input_password):
    return check_password_hash(db_password, input_password)
