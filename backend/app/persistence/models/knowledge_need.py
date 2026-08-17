from sqlalchemy import ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.persistence.database import Base
from app.persistence.models.knowledge import Knowledge


class KnowledgeNeed(Base):
    __tablename__ = "knowledge_needs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scope_id: Mapped[int] = mapped_column(
        ForeignKey("requirement_scopes.id", ondelete="CASCADE"), nullable=False
    )
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    depth: Mapped[int] = mapped_column(Integer, nullable=False)
    knowledge_id: Mapped[object | None] = mapped_column(
        Uuid(), ForeignKey("knowledge.id"), nullable=True
    )

    scope: Mapped["RequirementScope"] = relationship(back_populates="knowledge_needs")
    knowledge: Mapped[Knowledge | None] = relationship(lazy="joined")
