from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.persistence.database import Base
from app.persistence.models.knowledge import Knowledge

if TYPE_CHECKING:
    from app.persistence.models.study_programme import StudyProgrammeUnit


class KnowledgeNeed(Base):
    """What a candidate must know for a programme unit; valid even without knowledge."""

    __tablename__ = "knowledge_needs"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True, default=uuid4)
    unit_id: Mapped[UUID] = mapped_column(
        ForeignKey("study_programme_units.id", ondelete="CASCADE"), nullable=False
    )
    topic: Mapped[str] = mapped_column(String(1000), nullable=False)
    depth: Mapped[int] = mapped_column(Integer, nullable=False)
    knowledge_id: Mapped[UUID | None] = mapped_column(
        Uuid(), ForeignKey("knowledge.id"), nullable=True
    )

    unit: Mapped[StudyProgrammeUnit] = relationship(back_populates="knowledge_needs")
    knowledge: Mapped[Knowledge | None] = relationship(lazy="joined")
