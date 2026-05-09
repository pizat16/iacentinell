import hashlib

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_string(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))
