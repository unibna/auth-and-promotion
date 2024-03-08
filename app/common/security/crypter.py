import bcrypt
import hashlib
from loguru import logger
import os
import re


class Crypter:

    SALT = None

    def __init__(self):
        self.setup()

    def setup(self):
        self._load_salt()
    
    @classmethod
    def _load_salt(cls):
        """
        Should store SALT in vault in production
        """
        logger.info("loading salt")
        cls.SALT = bytes.fromhex(os.getenv("HASH_PASSWORD_SALT"))
        logger.success("loading salt successfully")

    @classmethod
    def hash_password(cls, plaintext: str) -> str:
        if not cls.SALT:
            cls._load_salt()
        return bcrypt.hashpw(plaintext, cls.SALT)
    
    @classmethod
    def hash(cls, plaintext: str) -> str:
        return hashlib.sha256(plaintext.encode()).hexdigest()
    
    @classmethod
    def is_hashed(cls, value: str) -> bool:
        bcrypt_pattern = re.compile(r'^\$\d+\$[a-zA-Z0-9./]+$', re.ASCII)
        return bool(bcrypt_pattern.match(value))


crypter = Crypter()
