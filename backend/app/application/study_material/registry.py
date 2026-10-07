"""Registry of supported study topics (the single place to add a new topic)."""

from app.application.study_material.topic import StudyTopic
from app.application.study_material.topics import (
    access,
    civil_servants,
    civil_servants_rights,
    constitution,
    constitutional_court_and_crown,
    cortes_generales,
    data_modeling,
    government,
    identity,
    judicial_power,
    object_oriented,
    personal_data,
    procedure,
    state_administration,
    state_budget,
    territorial_organisation,
)

TOPICS: tuple[StudyTopic, ...] = (
    access.TOPIC,
    procedure.TOPIC,
    identity.TOPIC,
    personal_data.TOPIC,
    object_oriented.TOPIC,
    data_modeling.TOPIC,
    constitution.TOPIC,
    constitutional_court_and_crown.TOPIC,
    cortes_generales.TOPIC,
    judicial_power.TOPIC,
    government.TOPIC,
    state_administration.TOPIC,
    territorial_organisation.TOPIC,
    civil_servants.TOPIC,
    civil_servants_rights.TOPIC,
    state_budget.TOPIC,
)


def find_topic_by_name(name: str) -> StudyTopic | None:
    return next((topic for topic in TOPICS if topic.name == name), None)


def find_topic_for_title(title: str) -> StudyTopic | None:
    normalized_title = title.casefold()
    return next((topic for topic in TOPICS if topic.matches(normalized_title)), None)
