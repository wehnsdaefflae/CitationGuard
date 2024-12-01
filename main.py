from cpi.formatters import TemplateFormatter
from cpi.models import Citation
from cpi.providers import BasicCitationProvider
from msi.embedding import MockEmbeddingProvider
from msi.providers import BasicSemanticProvider
from ssi.encryption import FernetEncryptionProvider
from ssi.models import Source, AccessPolicy
from ssi.providers import InMemorySourceProvider


def main() -> None:
    # Initialize components
    encryption_provider = FernetEncryptionProvider()
    source_provider = InMemorySourceProvider(encryption_provider)

    embedding_provider = MockEmbeddingProvider()
    semantic_provider = BasicSemanticProvider(embedding_provider)

    citation_formatter = TemplateFormatter()
    citation_provider = BasicCitationProvider(citation_formatter)

    # Example workflow
    async def example():
        # Store source
        source = Source(
            content=b"Example confidential source content",
            metadata={"title": "Secret Document"}
        )
        policy = AccessPolicy(
            level="confidential",
            allowed_users=["researcher1"],
            encryption_scheme="fernet"
        )
        source_id = await source_provider.store(source, policy)

        # Create semantic index
        text = "Example content for semantic matching"
        index = await semantic_provider.index(text, "en")

        # Format citation
        citation = Citation(
            source_id=source_id,
            style="apa",
            context={
                "authors": "Smith, J.",
                "year": "2024",
                "title": "Confidential Research"
            }
        )
        formatted = await citation_provider.format(citation)
        print(f"Formatted citation: {formatted}")

    # Run example
    import asyncio
    asyncio.run(example())


if __name__ == "__main__":
    main()
