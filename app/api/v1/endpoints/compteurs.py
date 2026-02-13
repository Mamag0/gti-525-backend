from datetime import datetime

from fastapi import APIRouter, HTTPException, Path, Query

from app.services.sqlite_service import fetch_compteur_period

router = APIRouter(prefix="/compteurs", tags=["compteurs"])


def _parse_yyyymmdd(value: str, field_name: str) -> str:
    try:
        parsed = datetime.strptime(value, "%Y%m%d")
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=f"{field_name} doit etre au format YYYYMMDD",
        ) from exc
    return parsed.strftime("%Y-%m-%d")


@router.get("/{id_compteur}")
def get_compteur_by_period(
    id_compteur: int = Path(..., ge=1),
    debut: str = Query(..., pattern=r"^\d{8}$"),
    fin: str = Query(..., pattern=r"^\d{8}$"),
) -> dict[str, object]:
    debut_iso = _parse_yyyymmdd(debut, "debut")
    fin_iso = _parse_yyyymmdd(fin, "fin")

    if debut_iso > fin_iso:
        raise HTTPException(status_code=422, detail="debut doit etre <= fin")

    items = fetch_compteur_period(id_compteur=id_compteur, debut_iso=debut_iso, fin_iso=fin_iso)
    total_passages = sum(int(item["nb_passages"]) for item in items)

    return {
        "id_compteur": id_compteur,
        "debut": debut,
        "fin": fin,
        "count": len(items),
        "total_passages": total_passages,
        "items": items,
    }
