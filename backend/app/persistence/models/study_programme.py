from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.persistence.database import Base


class StudyProgramme(Base):
    __tablename__ = "study_programmes"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True, default=uuid4)
    call_id: Mapped[UUID] = mapped_column(
        ForeignKey("calls.id", ondelete="CASCADE"), nullable=False
    )
    identifier: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    units: Mapped[list["StudyProgrammeUnit"]] = relationship(
        back_populates="programme",
        cascade="all, delete-orphan",
        order_by="StudyProgrammeUnit.number",
        lazy="selectin",
    )


class StudyProgrammeUnit(Base):
    __tablename__ = "study_programme_units"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True, default=uuid4)
    programme_id: Mapped[UUID] = mapped_column(
        ForeignKey("study_programmes.id", ondelete="CASCADE"), nullable=False
    )
    number: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(1000), nullable=False)
    start_page: Mapped[int] = mapped_column(nullable=False)
    start_order: Mapped[int] = mapped_column(nullable=False)
    end_page: Mapped[int] = mapped_column(nullable=False)
    end_order: Mapped[int] = mapped_column(nullable=False)

    programme: Mapped[StudyProgramme] = relationship(back_populates="units")
