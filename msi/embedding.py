from abc import ABC, abstractmethod
from typing import List
import numpy as np
from numpy.typing import NDArray


class EmbeddingProvider(ABC):
    """Base class for text embedding providers."""

    @abstractmethod
    def embed(self, text: str, language: str) -> NDArray:
        """Generate embeddings for text in specified language."""
        pass

    @abstractmethod
    def similarity(self, embedding1: NDArray, embedding2: NDArray) -> float:
        """Calculate similarity between two embeddings."""
        pass


class MockEmbeddingProvider(EmbeddingProvider):
    """Mock embedding provider for development/testing."""

    def embed(self, text: str, language: str) -> NDArray:
        """Generate mock embeddings (random vectors)."""
        # In real implementation, use proper language models
        return np.random.rand(384)  # Common embedding size

    def similarity(self, embedding1: NDArray, embedding2: NDArray) -> float:
        """Calculate cosine similarity between embeddings."""
        return float(np.dot(embedding1, embedding2) /
                     (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))
