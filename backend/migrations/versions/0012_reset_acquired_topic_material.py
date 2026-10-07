"""Drop cached curated material for topics now acquired from authoritative sources.

Ley 19/2013 and Ley 39/2015 study material used to be hand-written text cached
as Knowledge. It is now assembled from the BOE articles, so the stale cached
copies are removed and regenerated (with provenance) on next use.

Revision ID: 0012_reset_acquired_topic_material
Revises: 0011_knowledge_sources
Create Date: 2026-10-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0012_reset_acquired_topic_material"
down_revision: str | Sequence[str] | None = "0011_knowledge_sources"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_IDENTITY_SEPARATOR = "\x1f"
_ACQUIRED_TOPICS = (
    "Derecho de acceso a la información pública",
    "Procedimiento administrativo común",
)


def upgrade() -> None:
    connection = op.get_bind()
    for topic in _ACQUIRED_TOPICS:
        params = {"identity_key": f"{topic}{_IDENTITY_SEPARATOR}1"}
        stale = "(SELECT id FROM knowledge WHERE identity_key = :identity_key)"
        connection.execute(
            sa.text(f"UPDATE knowledge_needs SET knowledge_id = NULL WHERE knowledge_id IN {stale}"),
            params,
        )
        connection.execute(
            sa.text(f"DELETE FROM knowledge_sources WHERE knowledge_id IN {stale}"), params
        )
        connection.execute(sa.text("DELETE FROM knowledge WHERE identity_key = :identity_key"), params)


def downgrade() -> None:
    """Deleted cache entries are regenerated on demand; nothing to restore."""
