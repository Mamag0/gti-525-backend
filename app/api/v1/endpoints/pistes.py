from fastapi import APIRouter, HTTPException

from app.services.data_files_service import load_reseau_cyclable_geojson

router = APIRouter(tags=["pistes"])


@router.get("/pistes")
def get_pistes() -> dict[str, object]:
    try:
        return load_reseau_cyclable_geojson()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="reseau_cyclable.geojson introuvable") from exc
