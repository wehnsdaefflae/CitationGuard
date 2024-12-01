from abc import ABC, abstractmethod
from typing import Dict, List
from .models import Citation, CitationStyle
from .formatters import CitationFormatter


class CitationProvider(ABC):
    """Abstract base class for citation providers."""

    def __init__(self, formatter: CitationFormatter):
        self.formatter = formatter
        self.styles: Dict[str, CitationStyle] = {}

    @abstractmethod
    async def format(self, citation: Citation) -> str:
        """Format citation according to style guide."""
        pass

    @abstractmethod
    async def validate(self, citation: Citation) -> bool:
        """Validate citation integrity and permissions."""
        pass


class BasicCitationProvider(CitationProvider):
    """Basic implementation of citation provider."""

    def __init__(self, formatter: CitationFormatter):
        super().__init__(formatter)
        self._init_default_styles()

    def _init_default_styles(self):
        """Initialize default citation styles."""
        self.styles["apa"] = CitationStyle(
            name="APA",
            template="{authors} ({year}). {title}. {publisher}.",
            required_fields=["authors", "year", "title"],
            optional_fields=["publisher", "doi"]
        )

        self.styles["journalism"] = CitationStyle(
            name="Journalism",
            template='"{quote}" ({source}, {date})',
            required_fields=["source", "date"],
            optional_fields=["quote"]
        )

    async def format(self, citation: Citation) -> str:
        """Format citation using specified style."""
        if citation.style not in self.styles:
            raise ValueError(f"Unknown citation style: {citation.style}")

        style = self.styles[citation.style]
        return self.formatter.format(citation, style)

    async def validate(self, citation: Citation) -> bool:
        """Basic citation validation."""
        if citation.style not in self.styles:
            return False

        style = self.styles[citation.style]
        return all(field in citation.context for field in style.required_fields)

