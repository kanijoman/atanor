"""Allow legacy knowledge records without a business identity.

Revision ID: 0010_knowledge_identity_optional
Revises: 0009_knowledge_identity
Create Date: 2026-09-15
"""

from typing import Sequence, Union

from alembic import op

revision: str = "0010_knowledge_identity_optional"
down_revision: Union[str, Sequence[str], None] = "0009_knowledge_identity"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("knowledge") as batch_op:
        batch_op.alter_column("identity_key", nullable=True)


def downgrade() -> None:
    with op.batch_alter_table("knowledge") as batch_op:
        batch_op.alter_column("identity_key", nullable=False)
