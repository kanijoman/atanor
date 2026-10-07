"""Identify sources by the hash of their content.

A source used to be identified only by its local path, so renaming or moving a
file created a duplicate source and call. The SHA-256 of the document makes
imports idempotent regardless of where the file lives. Existing sources keep a
NULL hash until they are imported again.

Revision ID: 0013_source_content_hash
Revises: 0012_reset_acquired_topic_material
Create Date: 2026-10-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0013_source_content_hash"
down_revision: str | Sequence[str] | None = "0012_reset_acquired_topic_material"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("sources") as batch_op:
        batch_op.add_column(sa.Column("content_hash", sa.String(length=64), nullable=True))
        batch_op.create_unique_constraint("uq_sources_content_hash", ["content_hash"])


def downgrade() -> None:
    with op.batch_alter_table("sources") as batch_op:
        batch_op.drop_constraint("uq_sources_content_hash", type_="unique")
        batch_op.drop_column("content_hash")
