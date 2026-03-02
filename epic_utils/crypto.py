from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import uuid

class PasswordManager:
    _hasher = PasswordHasher()
    @staticmethod
    def hash(password: str):
        hash = PasswordManager._hasher.hash(password)
        return hash

    @staticmethod
    def check_password(hash: str, password: str):
        try:
            PasswordManager._hasher.verify(hash, password)
        except VerifyMismatchError:
            return False    
        return True
    
    @staticmethod
    def create_key():
        return str(uuid.uuid4())