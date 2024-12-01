import base64
from abc import ABC, abstractmethod
from typing import Any, Dict
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionProvider(ABC):
    """Base class for encryption providers."""

    @abstractmethod
    def encrypt(self, data: bytes, context: Dict[str, Any]) -> bytes:
        """Encrypt data using the specified context."""
        pass

    @abstractmethod
    def decrypt(self, encrypted_data: bytes, context: Dict[str, Any]) -> bytes:
        """Decrypt data using the specified context."""
        pass


class FernetEncryptionProvider(EncryptionProvider):
    """Basic encryption provider using Fernet (for development/testing)."""

    def __init__(self, salt: bytes = None):
        self.salt = salt or os.urandom(16)

    def _get_key(self, context: Dict[str, Any]) -> bytes:
        """Derive key from context using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = kdf.derive(str(context).encode())
        return base64.b64encode(key)

    def encrypt(self, data: bytes, context: Dict[str, Any]) -> bytes:
        key = self._get_key(context)
        f = Fernet(key)
        return f.encrypt(data)

    def decrypt(self, encrypted_data: bytes, context: Dict[str, Any]) -> bytes:
        key = self._get_key(context)
        f = Fernet(key)
        return f.decrypt(encrypted_data)
