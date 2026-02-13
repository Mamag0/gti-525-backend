from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.services.sqlite_service import ensure_schema, get_connection

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/gti525/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_compteur_period_route_shape(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(settings, "SQLITE_DB_PATH", str(db_path))
    ensure_schema()

    with get_connection() as conn:
        conn.executemany(
            """
            INSERT INTO comptage_velo (date_heure, id_compteur, nb_passages)
            VALUES (?, ?, ?)
            """,
            [
                ("2022-01-01 00:00:00", 100054585, 5),
                ("2022-01-15 10:00:00", 100054585, 7),
                ("2022-02-01 00:00:00", 100054585, 99),
            ],
        )
        conn.commit()

    response = client.get("/gti525/v1/compteurs/100054585?debut=20220101&fin=20220131")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id_compteur"] == 100054585
    assert payload["debut"] == "20220101"
    assert payload["fin"] == "20220131"
    assert payload["count"] == 2
    assert payload["total_passages"] == 12


def test_pistes_returns_geojson(tmp_path: Path, monkeypatch) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    geojson_file = input_dir / "reseau_cyclable.geojson"
    geojson_file.write_text('{"type":"FeatureCollection","features":[]}', encoding="utf-8")
    monkeypatch.setattr(settings, "INPUT_DATA_DIR", input_dir)

    response = client.get("/gti525/v1/pistes")

    assert response.status_code == 200
    assert response.json()["type"] == "FeatureCollection"


def test_pointsdinteret_returns_csv_as_json(tmp_path: Path, monkeypatch) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    csv_file = input_dir / "fontaines.csv"
    csv_file.write_text("id,nom\n1,Fontaine A\n2,Fontaine B\n", encoding="utf-8")
    monkeypatch.setattr(settings, "INPUT_DATA_DIR", input_dir)

    response = client.get("/gti525/v1/pointsdinteret")

    assert response.status_code == 200
    assert response.json() == [
        {"id": "1", "nom": "Fontaine A"},
        {"id": "2", "nom": "Fontaine B"},
    ]
