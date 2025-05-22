from fastapi import APIRouter

from app.dashboard.adapter.input.api.v1.dashboard import dashboard_router as dashboard_v1_router

router = APIRouter()
router.include_router(dashboard_v1_router, prefix="/api/v1/dashboard", tags=["Dashboard"])

__all__ = ["router"]
