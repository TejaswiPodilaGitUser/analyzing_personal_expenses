import bcrypt

def hash_password(password):
    """
    Hashes a password using bcrypt.
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed

def check_password(password, hashed):
    """
    Checks a password against a hashed password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
