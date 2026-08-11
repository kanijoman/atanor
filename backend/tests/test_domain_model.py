from app.domain.models import Blueprint, Knowledge, Requirement, Source


def test_closed_source_requirement_can_define_required_knowledge() -> None:
    constitution = Source(
        title="Spanish Constitution",
        locator="https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229",
    )
    article_one = Knowledge(
        title="Article 1 of the Spanish Constitution",
        description="The first article of the Spanish Constitution.",
        sources=(constitution,),
    )

    requirement = Requirement(
        title="Article 1 of the Spanish Constitution",
    )
    blueprint = Blueprint().requires(article_one)
    requirement = requirement.with_source(constitution).with_blueprint(blueprint)

    assert requirement.sources == (constitution,)
    assert requirement.blueprint is blueprint
    assert requirement.blueprint.requirements == (article_one,)
    assert article_one.sources == (constitution,)
