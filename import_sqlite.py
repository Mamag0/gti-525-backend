import argparse
import csv
import glob
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path("comptage_velo.db")
CSV_GLOB = "comptage_velo_*.csv"


def ensure_schema(conn: sqlite3.Connection) -> None:
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


def import_file(conn: sqlite3.Connection, csv_path: Path) -> int:
    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = [
            (row["date_heure"], int(row["id_compteur"]), int(row["nb_passages"]))
            for row in reader
        ]

    if not rows:
        return 0

    conn.executemany(
        """
        INSERT INTO comptage_velo (date_heure, id_compteur, nb_passages)
        VALUES (?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    return len(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import comptage_velo CSV files into SQLite.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("."),
        help="Directory containing comptage_velo_*.csv files.",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Path to SQLite database file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = args.input_dir
    db_path = args.db_path

    csv_files = sorted(Path(file) for file in glob.glob(str(input_dir / CSV_GLOB)))
    if not csv_files:
        print(f"No CSV files found in {input_dir} with pattern: {CSV_GLOB}")
        return

    with sqlite3.connect(db_path) as conn:
        ensure_schema(conn)
        total = 0
        for csv_file in csv_files:
            inserted = import_file(conn, csv_file)
            total += inserted
            print(f"Inserted {inserted} rows from {csv_file}")

    print(f"Import completed. Total rows inserted: {total}. DB: {db_path}")


if __name__ == "__main__":
    main()
