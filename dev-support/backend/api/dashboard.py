from fastapi import APIRouter

from backend.services.dashboardservice import (
    get_dashboard_stats
)

router = APIRouter()


@router.get("/dashboard")
def dashboard():

    return get_dashboard_stats()