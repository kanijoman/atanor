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
    with op.batch_alter_table("requirements") as batch_op:
        batch_op.add_column(
            sa.Column("source_id", sa.Uuid(), nullable=False),
        )
        batch_op.create_foreign_key(
            "fk_requirements_source_id_sources",
            "sources",
            ["source_id"],
            ["id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("requirements") as batch_op:
        batch_op.drop_constraint(
            "fk_requirements_source_id_sources",
            type_="foreignkey",
        )
        batch_op.drop_column("source_id")
