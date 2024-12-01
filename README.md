# CitationGuard

Foundational infrastructure components for building secure source management and citation systems. CitationGuard enables developers to add secure citation capabilities to any application while maintaining source confidentiality through homomorphic encryption.

## Core Components

### 1. Secure Source Infrastructure (SSI)
Privacy-preserving source storage and search infrastructure:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Source:
    content: bytes
    metadata: dict

@dataclass
class AccessPolicy:
    level: str
    allowed_users: List[str]
    encryption_scheme: str

class SecureSourceProvider(ABC):
    @abstractmethod
    async def store(self, source: Source, policy: AccessPolicy) -> str:
        """Store source securely and return source ID."""
        pass

    @abstractmethod
    async def search(self, query: str, security_context: dict) -> List[Source]:
        """Search sources within security context."""
        pass
```

Features:
- Homomorphic encryption for source protection
- Fine-grained access control
- Air-gapped operation support
- Cross-platform protocol support
- Backup and versioning capabilities

### 2. Multilingual Semantic Infrastructure (MSI)
Privacy-preserving semantic matching infrastructure:

```python
from numpy.typing import NDArray

class SemanticProvider(ABC):
    @abstractmethod
    async def index(self, content: str, language: str) -> NDArray:
        """Create privacy-preserving vector index."""
        pass

    @abstractmethod
    async def match(self, query: str, indices: List[NDArray]) -> List[float]:
        """Find semantic matches across indices."""
        pass
```

Features:
- Privacy-preserving vector indices using Microsoft SEAL
- Pluggable language model support
- Cross-lingual matching
- Customizable similarity metrics
- Batch processing support

### 3. Citation Protocol Infrastructure (CPI)
Framework for standardized citation handling:

```python
@dataclass
class Citation:
    source_id: str
    style: str
    context: dict

class CitationProvider(ABC):
    @abstractmethod
    async def format(self, citation: Citation) -> str:
        """Format citation according to style guide."""
        pass

    @abstractmethod
    async def validate(self, citation: Citation) -> bool:
        """Validate citation integrity and permissions."""
        pass
```

Features:
- Academic, journalistic, and legal citation formats
- Style guide automation
- Citation integrity verification
- Source anonymization options
- Batch citation processing

## Installation

```bash
pip install citation-guard[all]  # Install all components
# Or install individual components:
pip install citation-guard-ssi   # Secure Source Infrastructure
pip install citation-guard-msi   # Multilingual Semantic Infrastructure
pip install citation-guard-cpi   # Citation Protocol Infrastructure
```

## Quick Start

```python
from citation_guard.ssi import SecureSourceProvider
from citation_guard.msi import SemanticProvider
from citation_guard.cpi import CitationProvider

# Initialize components
source_provider = SecureSourceProvider(
    encryption="homomorphic",
    policy="need-to-know"
)

semantic_provider = SemanticProvider(
    languages=["en", "de"],
    privacy_preserving=True
)

# Store secure source
source_id = await source_provider.store(
    source=Source(content=my_content, metadata=my_metadata),
    policy=AccessPolicy(
        level="confidential",
        allowed_users=["researcher1", "journalist2"],
        encryption_scheme="seal-ckks"
    )
)

# Search within security context
matches = await semantic_provider.match(
    query="my search query",
    indices=await source_provider.get_indices(security_context)
)
```

## Documentation

Visit [docs.citation-guard.dev](https://docs.citation-guard.dev) for:
- Comprehensive API Reference
- Security Best Practices
- Integration Patterns
- Example Applications
- Deployment Guides

## Development Setup

```bash
# Clone repository
git clone https://github.com/citation-guard/citation-guard.git
cd citation-guard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Contributing

We welcome contributions! Please see:
- [Contributing Guidelines](CONTRIBUTING.md) for development practices
- [Code of Conduct](CODE_OF_CONDUCT.md) for community guidelines
- [Security Policy](SECURITY.md) for reporting security issues
- [Project Roadmap](ROADMAP.md) for planned features

## License

CitationGuard is released under the MIT License. See [LICENSE](LICENSE) file for details.