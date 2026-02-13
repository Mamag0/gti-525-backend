# FastAPI Backend GTI525

## Structure

- `app/main.py` entrypoint FastAPI
- `app/api/v1/router.py` routeur API v1
- `app/api/v1/endpoints/` endpoint `health`, `compteurs`, `pistes`, `pointsdinteret`
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

## Endpoints

- `GET /`
- `GET /gti525/v1/health`
- `GET /gti525/v1/pistes`
- `GET /gti525/v1/pointsdinteret`
- `GET /gti525/v1/compteurs/{id_compteur}?debut=YYYYMMDD&fin=YYYYMMDD`
- docs: `http://127.0.0.1:8000/docs`

## Tests

```powershell
pytest -q
```
