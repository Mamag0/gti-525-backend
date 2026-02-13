from collections.abc import Sequence
import sqlite3

from app.core.config import settings


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS comptage_velo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_heure TEXT NOT NULL,
                id_compteur INTEGER NOT NULL,
                nb_passages INTEGER NOT NULL
            )
            """
        )
        conn.commit()


def fetch_comptage_velo(limit: int = 100, offset: int = 0) -> list[dict[str, object]]:
    ensure_schema()
    with get_connection() as conn:
        rows: Sequence[sqlite3.Row] = conn.execute(
            """
            SELECT id, date_heure, id_compteur, nb_passages
            FROM comptage_velo
            ORDER BY id
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()

    return [dict(row) for row in rows]


def count_comptage_velo() -> int:
    ensure_schema()
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS total FROM comptage_velo").fetchone()

    return int(row["total"]) if row else 0


def fetch_compteur_period(id_compteur: int, debut_iso: str, fin_iso: str) -> list[dict[str, object]]:
    ensure_schema()
    with get_connection() as conn:
        rows: Sequence[sqlite3.Row] = conn.execute(
            """
            SELECT date_heure, id_compteur, nb_passages
            FROM comptage_velo
            WHERE id_compteur = ?
              AND date(date_heure) BETWEEN date(?) AND date(?)
            ORDER BY date_heure
            """,
            (id_compteur, debut_iso, fin_iso),
        ).fetchall()

    return [dict(row) for row in rows]
