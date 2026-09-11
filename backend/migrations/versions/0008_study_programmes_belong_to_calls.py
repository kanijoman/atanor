"""Associate study programmes with examination calls.

Revision ID: 0008_study_programmes_belong_to_calls
Revises: 0007_calls
Create Date: 2026-09-09
"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

revision: str = "0008_study_programmes_belong_to_calls"
down_revision: Union[str, Sequence[str], None] = "0007_calls"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    op.add_column(
        "study_programmes",
        sa.Column("call_id", sa.Uuid(), nullable=True),
    )

    sources = connection.execute(
        sa.text("SELECT id, title FROM sources")
    ).mappings().all()
    calls_by_source = {
        row["source_id"]: row["id"]
        for row in connection.execute(
            sa.text("SELECT id, source_id FROM calls ORDER BY id")
        ).mappings().all()
    }

    programme_source_ids = [
        row["source_id"]
        for row in connection.execute(
            sa.text("SELECT DISTINCT source_id FROM study_programmes")
        ).mappings().all()
    ]

    for source_id in programme_source_ids:
        call_id = calls_by_source.get(source_id)
        if call_id is None:
            source_title = next(
                row["title"] for row in sources if row["id"] == source_id
            )
            call_id = uuid4()
            connection.execute(
                sa.text(
                    "INSERT INTO calls (id, source_id, title) "
                    "VALUES (:id, :source_id, :title)"
                ),
                {"id": call_id, "source_id": source_id, "title": source_title},
            )
            calls_by_source[source_id] = call_id

        connection.execute(
            sa.text(
                "UPDATE study_programmes "
                "SET call_id = :call_id "
                "WHERE source_id = :source_id"
            ),
            {"call_id": call_id, "source_id": source_id},
        )

    with op.batch_alter_table("study_programmes") as batch_op:
        batch_op.alter_column("call_id", nullable=False)
        batch_op.drop_column("source_id")
        batch_op.create_foreign_key(
            "study_programmes_call_id_fkey",
            "calls",
            ["call_id"],
            ["id"],
            ondelete="CASCADE",
        )


def downgrade() -> None:
    with op.batch_alter_table("study_programmes") as batch_op:
        batch_op.add_column(sa.Column("source_id", sa.Uuid(), nullable=True))

    connection = op.get_bind()
    connection.execute(
        sa.text(
            "UPDATE study_programmes "
            "SET source_id = (SELECT source_id FROM calls WHERE calls.id = study_programmes.call_id)"
        )
    )

    with op.batch_alter_table("study_programmes") as batch_op:
        batch_op.alter_column("source_id", nullable=False)
        batch_op.drop_column("call_id")
        batch_op.create_foreign_key(
            "study_programmes_source_id_fkey",
            "sources",
            ["source_id"],
            ["id"],
            ondelete="CASCADE",
        )
