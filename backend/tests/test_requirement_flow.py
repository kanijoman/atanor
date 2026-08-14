from pathlib import Path
from uuid import uuid4

import pytest

from app.application.requirement import PdfRequirementDiscoveryStrategy
from app.application.requirement import discover_and_resolve_requirements
from app.domain.models import Requirement, Source
from app.domain.requirement_resolution import (
    RequirementCandidate,
    RequirementResolutionStatus,
    resolve_requirement,
)


SAMPLE_NAMES = (
    "BOE-A-2024-14098.pdf",
    "OPOS_AYTO_LEON_INFORMATICA_B.pdf",
    "Programa_Archiveros_0.pdf",
)

TEXT_SAMPLES = (
    "BOE-A-2024-14098.pdf",
    "Programa_Archiveros_0.pdf",
)


def test_requirement_resolution_flow_starts_from_a_source_candidate() -> None:
    samples_dir = Path(__file__).parent / "samples"

    for sample_name in SAMPLE_NAMES:
        sample_path = samples_dir / sample_name
        assert sample_path.is_file()

        source_id = uuid4()
        candidate = RequirementCandidate(
            title=f"Requirement from {sample_name}",
            source_id=source_id,
        )
        requirement = Requirement(
            title=candidate.title,
            source_id=source_id,
        )

        resolution = resolve_requirement(candidate, (requirement,))

        assert resolution.status is RequirementResolutionStatus.RESOLVED
        assert resolution.requirement is requirement
        assert resolution.candidate.source_id == source_id


def test_requirement_resolution_flow_identifies_an_unresolved_candidate() -> None:
    samples_dir = Path(__file__).parent / "samples"
    sample_path = samples_dir / SAMPLE_NAMES[0]
    assert sample_path.is_file()

    candidate = RequirementCandidate(
        title="Requirement not present in the knowledge model",
        source_id=uuid4(),
    )

    resolution = resolve_requirement(candidate, ())

    assert resolution.status is RequirementResolutionStatus.UNRESOLVED
    assert resolution.requirement is None
    assert resolution.candidate is candidate


def test_requirement_resolution_flow_identifies_ambiguous_candidate() -> None:
    samples_dir = Path(__file__).parent / "samples"
    sample_path = samples_dir / SAMPLE_NAMES[1]
    assert sample_path.is_file()

    candidate = RequirementCandidate(
        title="Operating Systems",
        source_id=uuid4(),
    )
    requirements = (
        Requirement(title="Operating Systems", source_id=uuid4()),
        Requirement(title="Operating Systems", source_id=uuid4()),
    )

    resolution = resolve_requirement(candidate, requirements)

    assert resolution.status is RequirementResolutionStatus.UNRESOLVED
    assert resolution.requirement is None
    assert resolution.candidate is candidate


@pytest.mark.parametrize("sample_name", TEXT_SAMPLES)
def test_discovery_and_resolution_are_integrated_for_supported_text_pdf_samples(
    sample_name: str,
) -> None:
    samples_dir = Path(__file__).parent / "samples"
    source_id = uuid4()
    source = Source(
        id=source_id,
        title=sample_name,
        locator=str(samples_dir / sample_name),
    )

    mentions = PdfRequirementDiscoveryStrategy().discover(source)
    assert mentions

    # The fixture requirements represent already validated knowledge entries.
    # The test verifies that discovery can cross the application boundary into
    # automatic resolution without requiring user validation.
    requirements = tuple(
        Requirement(title=mention.expression, source_id=source_id)
        for mention in mentions
    )

    resolutions = discover_and_resolve_requirements(
        source,
        PdfRequirementDiscoveryStrategy(),
        requirements,
    )

    assert len(resolutions) == len(mentions)
    assert all(
        resolution.status is RequirementResolutionStatus.RESOLVED
        for resolution in resolutions
    )
    assert all(
        resolution.candidate.source_id == source_id
        for resolution in resolutions
    )


def test_scanned_pdf_remains_an_explicitly_unsupported_discovery_input() -> None:
    samples_dir = Path(__file__).parent / "samples"
    source_id = uuid4()
    source = Source(
        id=source_id,
        title="OPOS_AYTO_LEON_INFORMATICA_B.pdf",
        locator=str(samples_dir / "OPOS_AYTO_LEON_INFORMATICA_B.pdf"),
    )

    mentions = PdfRequirementDiscoveryStrategy().discover(source)

    assert mentions == ()


def test_discovery_and_resolution_keep_unresolved_candidates_for_internal_curation() -> None:
    samples_dir = Path(__file__).parent / "samples"
    source_id = uuid4()
    source = Source(
        id=source_id,
        title=SAMPLE_NAMES[0],
        locator=str(samples_dir / SAMPLE_NAMES[0]),
    )

    mentions = PdfRequirementDiscoveryStrategy().discover(source)
    assert mentions

    resolutions = discover_and_resolve_requirements(
        source,
        PdfRequirementDiscoveryStrategy(),
        (),
    )

    assert len(resolutions) == len(mentions)
    assert all(
        resolution.status is RequirementResolutionStatus.UNRESOLVED
        for resolution in resolutions
    )
    assert all(
        resolution.requirement is None
        for resolution in resolutions
    )
    assert all(
        resolution.candidate.source_id == source_id
        for resolution in resolutions
    )
