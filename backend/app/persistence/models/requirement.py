from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.persistence.database import Base
from app.persistence.types import UTCDateTime


class Requirement(Base):
    __tablename__ = "requirements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_id: Mapped[UUID] = mapped_column(
        ForeignKey("sources.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime, nullable=False, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    scopes: Mapped[list["RequirementScope"]] = relationship(
        back_populates="requirement",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class RequirementScope(Base):
    __tablename__ = "requirement_scopes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    requirement_id: Mapped[int] = mapped_column(
        ForeignKey("requirements.id", ondelete="CASCADE"), nullable=False
    )
    context: Mapped[str] = mapped_column(Text, nullable=False)
    requirement: Mapped[Requirement] = relationship(back_populates="scopes")
    knowledge_needs: Mapped[list["KnowledgeNeed"]] = relationship(
        back_populates="scope",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class KnowledgeNeed(Base):
    __tablename__ = "knowledge_needs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scope_id: Mapped[int] = mapped_column(
        ForeignKey("requirement_scopes.id", ondelete="CASCADE"), nullable=False
    )
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    depth: Mapped[int] = mapped_column(Integer, nullable=False)
    scope: Mapped[RequirementScope] = relationship(back_populates="knowledge_needs")
