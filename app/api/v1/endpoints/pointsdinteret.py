from fastapi import APIRouter, HTTPException

from app.services.data_files_service import load_fontaines_as_json

router = APIRouter(tags=["pointsdinteret"])


@router.get("/pointsdinteret")
def get_pointsdinteret() -> list[dict[str, str]]:
    try:
        return load_fontaines_as_json()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="fontaines.csv introuvable") from exc
