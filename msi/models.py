from dataclasses import dataclass
from typing import List, Optional
import numpy as np
from numpy.typing import NDArray

@dataclass
class SemanticIndex:
    """Represents a privacy-preserving semantic index."""
    vector: NDArray
    language: str
    metadata: dict

@dataclass
class SemanticMatch:
    """Represents a semantic match result."""
    source_id: str
    score: float
    context: dict
