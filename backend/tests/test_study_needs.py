from pathlib import Path
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.dependencies import get_session_factory, get_uploads_dir
from app.application.study_needs import (
    attach_knowledge_needs,
    ensure_knowledge_needs,
    needs_for_unit,
)
from app.domain.models import Call, KnowledgeNeed, Source, StudyProgramme, StudyProgrammeUnit
from app.main import app
from app.persistence.call_repository import SqlAlchemyCallRepository
from app.persistence.database import Base
from app.persistence.source_repository import SqlAlchemySourceRepository
from app.persistence.study_programme_repository import SqlAlchemyStudyProgrammeRepository

SAMPLES = Path(__file__).parent / "samples"
SUPPORTED_TITLE = "Las Leyes del Procedimiento Administrativo Común de las Administraciones"
UNSUPPORTED_TITLE = "El modelo TCP/IP y el modelo de referencia de interconexión de sistemas"


def _unit(title: str, *needs: KnowledgeNeed) -> StudyProgrammeUnit:
    return StudyProgrammeUnit(
        number=1,
        title=title,
        start_page=1,
        start_order=1,
        end_page=1,
        end_order=2,
        knowledge_needs=needs,
    )


def test_supported_unit_needs_the_topic_atanor_can_prepare() -> None:
    [need] = needs_for_unit(_unit(SUPPORTED_TITLE))

    assert (need.topic, need.depth, need.knowledge) == (
        "Procedimiento administrativo común",
        1,
        None,
    )


def test_unsupported_unit_keeps_its_official_wording_as_the_need() -> None:
    [need] = needs_for_unit(_unit(UNSUPPORTED_TITLE))

    assert (need.topic, need.depth, need.knowledge) == (UNSUPPORTED_TITLE, 1, None)


def test_attaching_needs_covers_every_unit_and_keeps_existing_ones() -> None:
    existing = KnowledgeNeed(topic="Already decided", depth=1)
    programme = StudyProgramme(
        call_id=_unit("x").id,
        identifier="I",
        title="Programme",
        units=(_unit(SUPPORTED_TITLE), _unit(UNSUPPORTED_TITLE), _unit("Other", existing)),
    )

    attached = attach_knowledge_needs(programme)

    assert [len(unit.knowledge_needs) for unit in attached.units] == [1, 1, 1]
    assert attached.units[2].knowledge_needs == (existing,)


def _seed_legacy_unit(tmp_path: Path, title: str):
    engine = create_engine(f"sqlite:///{tmp_path / 'needs.db'}")
    Base.metadata.create_all(engine)
    return engine, sessionmaker(bind=engine), _unit(title)


def test_units_imported_before_needs_existed_get_them_when_first_read(tmp_path) -> None:

    engine, session_factory, unit = _seed_legacy_unit(tmp_path, SUPPORTED_TITLE)
    try:
        source = Source(title="Legacy", locator="legacy.pdf")
        SqlAlchemySourceRepository(session_factory).save(source)
        call = SqlAlchemyCallRepository(session_factory).save(
            Call(title="Legacy", source_id=source.id)
        )
        repository = SqlAlchemyStudyProgrammeRepository(session_factory)
        repository.save(StudyProgramme(call_id=call.id, identifier="I", title="P", units=(unit,)))
        legacy = repository.get_unit_by_id(unit.id)
        assert legacy is not None and legacy.knowledge_needs == ()

        ensured = ensure_knowledge_needs(legacy, repository)

        assert [need.topic for need in ensured.knowledge_needs] == [
            "Procedimiento administrativo común"
        ]
        reread = repository.get_unit_by_id(unit.id)
        assert reread is not None and len(reread.knowledge_needs) == 1
    finally:
        engine.dispose()


def test_imported_call_gives_every_unit_a_need_and_reading_material_links_knowledge(
    tmp_path,
) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'flow.db'}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    app.dependency_overrides[get_session_factory] = lambda: session_factory
    app.dependency_overrides[get_uploads_dir] = lambda: tmp_path / "uploads"
    try:
        client = TestClient(app)
        uploaded = client.post(
            "/api/calls",
            params={"filename": "boe.pdf"},
            content=(SAMPLES / "BOE-A-2024-14098.pdf").read_bytes(),
            headers={"Content-Type": "application/pdf"},
        )
        assert uploaded.status_code == 201
        repository = SqlAlchemyStudyProgrammeRepository(session_factory)
        [first, *_] = repository.list_by_call(UUID(uploaded.json()["id"]))
        units = first.units

        assert all(len(unit.knowledge_needs) == 1 for unit in units)
        supported = next(unit for unit in units if unit.knowledge_needs[0].topic != unit.title)
        unsupported = next(unit for unit in units if unit.knowledge_needs[0].topic == unit.title)
        assert supported.knowledge_needs[0].knowledge is None

        assert client.get(f"/api/study/units/{supported.id}").status_code == 200
        assert client.get(f"/api/study/units/{unsupported.id}").status_code == 422

        linked = repository.get_unit_by_id(supported.id)
        untouched = repository.get_unit_by_id(unsupported.id)
        assert linked is not None and linked.knowledge_needs[0].knowledge is not None
        assert untouched is not None and untouched.knowledge_needs[0].knowledge is None
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
