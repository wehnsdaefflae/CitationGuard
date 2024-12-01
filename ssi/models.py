from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Source:
    """Represents a secure source with encrypted content and metadata."""
    content: bytes
    metadata: Dict[str, str]
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    version: int = 1

@dataclass
class AccessPolicy:
    """Defines access control and encryption policies for sources."""
    level: str  # e.g., "confidential", "restricted", "public"
    allowed_users: List[str]
    encryption_scheme: str  # e.g., "seal-ckks", "seal-bfv"
    expiration: Optional[datetime] = None
    require_2fa: bool = False
