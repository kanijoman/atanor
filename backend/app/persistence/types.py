from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator


class UTCDateTime(TypeDecorator[datetime]):
    """Persist datetimes as UTC and return timezone-aware UTC values."""

    impl = DateTime
    cache_ok = True

    def process_bind_param(
        self, value: datetime | None, dialect
    ) -> datetime | None:
        if value is None:
            return None

        if value.tzinfo is None:
            raise ValueError("Datetime values must be timezone-aware")

        return value.astimezone(UTC).replace(tzinfo=None)

    def process_result_value(
        self, value: datetime | None, dialect
    ) -> datetime | None:
        if value is None:
            return None

        return value.replace(tzinfo=UTC)
