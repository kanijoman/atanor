"""Persist the business identity of generated knowledge.

Revision ID: 0009_knowledge_identity
Revises: 0008_study_programmes_belong_to_calls
Create Date: 2026-09-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0009_knowledge_identity"
down_revision: Union[str, Sequence[str], None] = "0008_study_programmes_belong_to_calls"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "knowledge",
        sa.Column("identity_key", sa.String(length=512), nullable=True),
    )

    connection = op.get_bind()
    connection.execute(
        sa.text(
            "UPDATE knowledge "
            "SET identity_key = title || :separator || :depth"
        ),
        {"separator": "\x1f", "depth": 1},
    )

    with op.batch_alter_table("knowledge") as batch_op:
        batch_op.alter_column("identity_key", nullable=False)


def downgrade() -> None:
    with op.batch_alter_table("knowledge") as batch_op:
        batch_op.drop_column("identity_key")
