"""Registry of supported study topics (the single place to add a new topic)."""

from app.application.study_material.topic import StudyTopic
from app.application.study_material.topics import (
    access,
    constitution,
    constitutional_court_and_crown,
    cortes_generales,
    data_modeling,
    identity,
    judicial_power,
    object_oriented,
    personal_data,
    procedure,
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
)


def find_topic_by_name(name: str) -> StudyTopic | None:
    return next((topic for topic in TOPICS if topic.name == name), None)


def find_topic_for_title(title: str) -> StudyTopic | None:
    normalized_title = title.casefold()
    return next((topic for topic in TOPICS if topic.matches(normalized_title)), None)
