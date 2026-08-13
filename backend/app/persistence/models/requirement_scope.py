from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.persistence.database import Base


class RequirementScope(Base):
    __tablename__ = "requirement_scopes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    requirement_id: Mapped[int] = mapped_column(
        ForeignKey("requirements.id", ondelete="CASCADE"), nullable=False
    )
    context: Mapped[str] = mapped_column(Text, nullable=False)

    requirement: Mapped["Requirement"] = relationship(back_populates="scopes")
    knowledge_needs: Mapped[list["KnowledgeNeed"]] = relationship(
        back_populates="scope",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
