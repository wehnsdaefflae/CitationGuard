from abc import ABC, abstractmethod
from typing import List, Dict
import numpy as np
from .models import SemanticIndex, SemanticMatch
from .embedding import EmbeddingProvider


class SemanticProvider(ABC):
    """Abstract base class for semantic matching providers."""

    def __init__(self, embedding_provider: EmbeddingProvider):
        self.embedding = embedding_provider

    @abstractmethod
    async def index(self, content: str, language: str) -> SemanticIndex:
        """Create privacy-preserving vector index."""
        pass

    @abstractmethod
    async def match(self, query: str, indices: List[SemanticIndex]) -> List[SemanticMatch]:
        """Find semantic matches across indices."""
        pass


class BasicSemanticProvider(SemanticProvider):
    """Basic implementation of semantic matching."""

    async def index(self, content: str, language: str) -> SemanticIndex:
        """Generate semantic index using embeddings."""
        vector = self.embedding.embed(content, language)
        return SemanticIndex(
            vector=vector,
            language=language,
            metadata={"length": len(content)}
        )

    async def match(self, query: str, indices: List[SemanticIndex]) -> List[SemanticMatch]:
        """Find matches using cosine similarity."""
        query_embedding = self.embedding.embed(query, "auto")

        matches = []
        for idx, index in enumerate(indices):
            score = self.embedding.similarity(query_embedding, index.vector)
            matches.append(SemanticMatch(
                source_id=str(idx),
                score=score,
                context={"language": index.language}
            ))

        return sorted(matches, key=lambda x: x.score, reverse=True)
