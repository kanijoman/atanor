from uuid import UUID, uuid4

from sqlalchemy import Column, ForeignKey, String, Table, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.persistence.database import Base
from app.persistence.models.source import Source


knowledge_sources = Table(
    "knowledge_sources",
    Base.metadata,
    Column(
        "knowledge_id",
        Uuid(),
        ForeignKey("knowledge.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "source_id",
        Uuid(),
        ForeignKey("sources.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Knowledge(Base):
    __tablename__ = "knowledge"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    identity_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    sources: Mapped[list[Source]] = relationship(
        secondary=knowledge_sources,
        lazy="selectin",
    )
