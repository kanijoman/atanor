"""Attach knowledge needs to study programme units and drop the requirement tables.

The product models a requirement as the study programme unit stated by the
convocatoria, so `requirements` and `requirement_scopes` are removed and
`knowledge_needs` hangs directly from `study_programme_units`. The removed
tables were never populated by a product flow; any rows they held (only
possible through the retired requirements CLI) are discarded.

Revision ID: 0014_knowledge_needs_per_unit
Revises: 0013_source_content_hash
Create Date: 2026-10-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0014_knowledge_needs_per_unit"
down_revision: str | Sequence[str] | None = "0013_source_content_hash"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_table("knowledge_needs")
    op.drop_table("requirement_scopes")
    op.drop_table("requirements")

    op.create_table(
        "knowledge_needs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("unit_id", sa.Uuid(), nullable=False),
        sa.Column("topic", sa.String(length=1000), nullable=False),
        sa.Column("depth", sa.Integer(), nullable=False),
        sa.Column("knowledge_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(["unit_id"], ["study_programme_units.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["knowledge_id"], ["knowledge.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("knowledge_needs")

    op.create_table(
        "requirements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("source_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["source_id"], ["sources.id"], name="fk_requirements_source_id_sources"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "requirement_scopes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("requirement_id", sa.Integer(), nullable=False),
        sa.Column("context", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "knowledge_needs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scope_id", sa.Integer(), nullable=False),
        sa.Column("topic", sa.String(length=255), nullable=False),
        sa.Column("depth", sa.Integer(), nullable=False),
        sa.Column("knowledge_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(["scope_id"], ["requirement_scopes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["knowledge_id"], ["knowledge.id"], name="fk_knowledge_needs_knowledge_id"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
