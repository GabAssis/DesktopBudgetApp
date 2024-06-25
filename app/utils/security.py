import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_input(data):

    if not data:
        return False
    pass
