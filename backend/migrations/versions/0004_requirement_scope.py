"""Persist requirement scopes and knowledge needs.

Revision ID: 0004_requirement_scope
Revises: 0003_requirement_sources
Create Date: 2026-08-13
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_requirement_scope"
down_revision: Union[str, Sequence[str], None] = "0003_requirement_sources"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("requirements") as batch_op:
        batch_op.drop_column("context")

    op.create_table(
        "requirement_scopes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("requirement_id", sa.Integer(), nullable=False),
        sa.Column("context", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["requirement_id"],
            ["requirements.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "knowledge_needs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scope_id", sa.Integer(), nullable=False),
        sa.Column("topic", sa.String(length=255), nullable=False),
        sa.Column("depth", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["scope_id"],
            ["requirement_scopes.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("knowledge_needs")
    op.drop_table("requirement_scopes")

    with op.batch_alter_table("requirements") as batch_op:
        batch_op.add_column(sa.Column("context", sa.Text(), nullable=True))
