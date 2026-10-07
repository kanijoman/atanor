"""Persist the sources that support a piece of knowledge.

The `knowledge_sources` association table was added to the persistence model
without a migration, so databases built through Alembic could not store
knowledge with sources. Databases created from the models already have it.

Revision ID: 0011_knowledge_sources
Revises: 0010_knowledge_identity_optional
Create Date: 2026-10-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0011_knowledge_sources"
down_revision: str | Sequence[str] | None = "0010_knowledge_identity_optional"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    if sa.inspect(op.get_bind()).has_table("knowledge_sources"):
        return
    op.create_table(
        "knowledge_sources",
        sa.Column("knowledge_id", sa.Uuid(), nullable=False),
        sa.Column("source_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["knowledge_id"], ["knowledge.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("knowledge_id", "source_id"),
    )


def downgrade() -> None:
    op.drop_table("knowledge_sources")
