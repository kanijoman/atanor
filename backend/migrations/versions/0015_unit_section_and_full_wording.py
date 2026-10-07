"""Keep the block of a programme unit and its complete official wording.

Programmes can restart numbering in each block (`I. ...`, `II. ...`), and a
unit's wording spans several lines. `section` stores the block name and `title`
becomes unbounded text so the full wording fits.

Revision ID: 0015_unit_section_and_full_wording
Revises: 0014_knowledge_needs_per_unit
Create Date: 2026-10-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0015_unit_section_and_full_wording"
down_revision: str | Sequence[str] | None = "0014_knowledge_needs_per_unit"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("study_programme_units") as batch_op:
        batch_op.add_column(sa.Column("section", sa.String(length=255), nullable=True))
        batch_op.alter_column(
            "title", existing_type=sa.String(length=1000), type_=sa.Text(), existing_nullable=False
        )


def downgrade() -> None:
    with op.batch_alter_table("study_programme_units") as batch_op:
        batch_op.alter_column(
            "title", existing_type=sa.Text(), type_=sa.String(length=1000), existing_nullable=False
        )
        batch_op.drop_column("section")
