"""Link requirements to their source.

Revision ID: 0003_requirement_sources
Revises: 0002_sources
Create Date: 2026-08-12
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_requirement_sources"
down_revision: Union[str, Sequence[str], None] = "0002_sources"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "requirements",
        sa.Column("source_id", sa.Uuid(), nullable=True),
    )
    op.create_foreign_key(
        "fk_requirements_source_id_sources",
        "requirements",
        "sources",
        ["source_id"],
        ["id"],
    )
    op.alter_column("requirements", "source_id", nullable=False)


def downgrade() -> None:
    op.drop_constraint(
        "fk_requirements_source_id_sources",
        "requirements",
        type_="foreignkey",
    )
    op.drop_column("requirements", "source_id")
