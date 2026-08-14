from pathlib import Path
from uuid import uuid4

from app.domain.models import Requirement
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
