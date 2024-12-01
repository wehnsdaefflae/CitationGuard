from abc import ABC, abstractmethod
from typing import Dict
from .models import Citation, CitationStyle


class CitationFormatter(ABC):
    """Base class for citation formatters."""

    @abstractmethod
    def format(self, citation: Citation, style: CitationStyle) -> str:
        """Format citation according to style."""
        pass


class TemplateFormatter(CitationFormatter):
    """Simple template-based citation formatter."""

    def format(self, citation: Citation, style: CitationStyle) -> str:
        """Format citation using template substitution."""
        # Verify required fields
        for field in style.required_fields:
            if field not in citation.context:
                raise ValueError(f"Missing required field: {field}")

        # Build context with optional fields
        context = {
            "source_id": citation.source_id,
            **citation.context
        }

        if citation.page_number:
            context["page"] = citation.page_number
        if citation.quote:
            context["quote"] = citation.quote

        # Format citation
        try:
            return style.template.format(**context)
        except KeyError as e:
            raise ValueError(f"Invalid field in template: {e}")
