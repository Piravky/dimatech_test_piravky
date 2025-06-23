from hashlib import sha256


def verify_signature(message, signature):
    return sha256(message.encode()).hexdigest() == signature