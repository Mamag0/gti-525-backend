# FastAPI Backend GTI525

## Structure

- `app/main.py` entrypoint FastAPI
- `app/api/v1/router.py` routeur API v1
- `app/api/v1/endpoints/` endpoint `health`, `comptage-velo`, `compteurs`, `pistes`, `pointsdinteret`
- `app/services/sqlite_service.py` acces SQLite
- `app/services/data_files_service.py` lecture fichiers d'entree
- `import_sqlite.py` import CSV -> SQLite
- `app/core/config.py` settings
- `tests/` tests API

## Run via docker

simplement ```docker compose up --build```

## Run local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

## Fichiers d'entree

Par defaut, les endpoints de fichiers lisent dans `public/input`:

- `reseau_cyclable.geojson` pour `GET /gti525/v1/pistes`
- `fontaines.csv` pour `GET /gti525/v1/pointsdinteret`

Tu peux changer le dossier via `INPUT_DATA_DIR` dans `.env`.

## Import des CSV dans SQLite

Place les fichiers CSV (`comptage_velo_*.csv`) a la racine du projet puis execute:

```powershell
python import_sqlite.py
```

Si tes CSV sont ailleurs (ex: `..\lab2_input\livrable2`), execute:

```powershell
python import_sqlite.py --input-dir ..\lab2_input\livrable2 --db-path comptage_velo.db
```

Cela cree/remplit `comptage_velo.db`.

## Endpoints

- `GET /`
- `GET /gti525/v1/health`
- `GET /gti525/v1/pistes`
- `GET /gti525/v1/pointsdinteret`
- `GET /gti525/v1/comptage-velo?limit=100&offset=0`
- `GET /gti525/v1/compteurs/{id_compteur}?debut=YYYYMMDD&fin=YYYYMMDD`
- docs: `http://127.0.0.1:8000/docs`

## Tests

```powershell
pytest -q
```
