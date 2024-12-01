import uuid
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
from .models import Source, AccessPolicy
from .encryption import EncryptionProvider


class SecureSourceProvider(ABC):
    """Abstract base class for secure source storage providers."""

    def __init__(self, encryption_provider: EncryptionProvider):
        self.encryption = encryption_provider

    @abstractmethod
    async def store(self, source: Source, policy: AccessPolicy) -> str:
        """Store source securely and return source ID."""
        pass

    @abstractmethod
    async def retrieve(self, source_id: str, security_context: Dict[str, Any]) -> Source:
        """Retrieve source if allowed by security context."""
        pass

    @abstractmethod
    async def search(self, query: str, security_context: Dict[str, Any]) -> List[Source]:
        """Search sources within security context."""
        pass


class InMemorySourceProvider(SecureSourceProvider):
    """In-memory implementation for development/testing."""

    def __init__(self, encryption_provider: EncryptionProvider):
        super().__init__(encryption_provider)
        self.sources: Dict[str, Dict] = {}

    async def store(self, source: Source, policy: AccessPolicy) -> str:
        """Store source with encryption."""
        source_id = str(uuid.uuid4())

        # Encrypt source content
        encrypted_content = self.encryption.encrypt(
            source.content,
            {"policy": policy.dict()}
        )

        # Store encrypted source
        self.sources[source_id] = {
            "content": encrypted_content,
            "metadata": source.metadata,
            "policy": policy.dict(),
            "created_at": source.created_at,
            "last_modified": source.last_modified,
            "version": source.version
        }

        return source_id

    async def retrieve(self, source_id: str, security_context: Dict[str, Any]) -> Source:
        """Retrieve and decrypt source if authorized."""
        if source_id not in self.sources:
            raise KeyError(f"Source {source_id} not found")

        stored = self.sources[source_id]
        policy = AccessPolicy(**stored["policy"])

        # Verify access
        if security_context.get("user") not in policy.allowed_users:
            raise PermissionError("Access denied")

        # Decrypt content
        decrypted_content = self.encryption.decrypt(
            stored["content"],
            {"policy": stored["policy"]}
        )

        return Source(
            content=decrypted_content,
            metadata=stored["metadata"],
            created_at=stored["created_at"],
            last_modified=stored["last_modified"],
            version=stored["version"]
        )
