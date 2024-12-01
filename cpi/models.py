from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class Citation:
    """Represents a citation with style and context."""
    source_id: str
    style: str  # e.g., "apa", "chicago", "journalism"
    context: Dict[str, str]
    page_number: Optional[str] = None
    quote: Optional[str] = None

@dataclass
class CitationStyle:
    """Defines formatting rules for citations."""
    name: str
    template: str
    required_fields: List[str]
    optional_fields: List[str]
