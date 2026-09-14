"""Inspect persisted data required by the candidate study-material flow."""

from sqlalchemy import text

from app.persistence.database import engine


QUERIES = {
    "calls": """
        SELECT id, title
        FROM calls
    """,
    "knowledge": """
        SELECT id, title
        FROM knowledge
    """,
    "knowledge_needs": """
        SELECT id, topic, knowledge_id
        FROM knowledge_needs
        WHERE topic LIKE '%Derecho de acceso%'
    """,
    "programme_units": """
        SELECT id, number, title
        FROM study_programme_units
        WHERE title LIKE '%19/2013%'
    """,
}


with engine.connect() as connection:
    print(f"Database: {engine.url}")

    for name, query in QUERIES.items():
        print(f"\n=== {name} ===")
        rows = connection.execute(text(query)).mappings().all()

        if not rows:
            print("(no rows)")
            continue

        for row in rows:
            print(dict(row))
