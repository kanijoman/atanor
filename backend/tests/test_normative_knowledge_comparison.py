from app.application.normative_source import (
    HttpSourceRetriever,
    OfficialNormativeSourceCatalog,
    extract_article,
    reconstruct_knowledge_from_article,
    compare_knowledge_content,
)


def test_compare_acquired_knowledge_with_reference_content() -> None:
    candidate = OfficialNormativeSourceCatalog().resolve("Ley 39/2015")
    assert candidate is not None

    retrieved = HttpSourceRetriever().retrieve(candidate)
    article = extract_article(retrieved, 1)
    assert article is not None

    acquired = reconstruct_knowledge_from_article(retrieved, article)
    reference = (
        "La Ley 39/2015 establece las bases del procedimiento administrativo común "
        "de las Administraciones Públicas y regula los requisitos de validez y "
        "eficacia de los actos administrativos."
    )

    comparison = compare_knowledge_content(acquired, reference)

    assert comparison.matched_aspects == (
        "procedimiento administrativo común",
        "requisitos de validez y eficacia",
    )
    assert comparison.missing_aspects == ()
