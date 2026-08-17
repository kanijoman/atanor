"""Persist knowledge and its availability on knowledge needs.

Revision ID: 0005_knowledge
Revises: 0004_requirement_scope
Create Date: 2026-08-17
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0005_knowledge"
down_revision: Union[str, Sequence[str], None] = "0004_requirement_scope"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "knowledge",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    with op.batch_alter_table("knowledge_needs") as batch_op:
        batch_op.add_column(sa.Column("knowledge_id", sa.Uuid(), nullable=True))
        batch_op.create_foreign_key(
            "fk_knowledge_needs_knowledge_id",
            "knowledge",
            ["knowledge_id"],
            ["id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("knowledge_needs") as batch_op:
        batch_op.drop_constraint(
            "fk_knowledge_needs_knowledge_id",
            type_="foreignkey",
        )
        batch_op.drop_column("knowledge_id")

    op.drop_table("knowledge")
