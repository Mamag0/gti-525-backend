from fastapi import APIRouter, Query

from app.services.sqlite_service import count_comptage_velo, fetch_comptage_velo

router = APIRouter(prefix="/comptage-velo", tags=["comptage-velo"])


@router.get("")
def list_comptage_velo(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
) -> dict[str, object]:
    items = fetch_comptage_velo(limit=limit, offset=offset)
    total = count_comptage_velo()
    return {"total": total, "count": len(items), "items": items}
