import hashlib


def gen_hash(text: str | bytes, size: int = 32):
    if not isinstance(text, bytes):
        text = text.encode("utf-8")

    return hashlib.sha256(text).hexdigest()[:size]
