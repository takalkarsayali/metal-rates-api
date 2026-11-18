
from datetime import date

from fastapi import APIRouter, HTTPException, Query

from app.services.rate_store import (
    get_latest_rates,
    get_rates_by_date
)

router = APIRouter(
    prefix="/api/v1/rates",
    tags=["Metal Rates"]
)


@router.get("/latest")
def latest_rates():
    data = get_latest_rates()

    if not data or data.get("status") == "not_fetched":
        raise HTTPException(
            status_code=404,
            detail="No rates have been fetched yet."
        )

    return data


@router.get("/")
def rates_by_date(rate_date: date = Query(..., alias="date")):
    data = get_rates_by_date(rate_date)

    if data is None:
        raise HTTPException(
            status_code=404,
            detail=f"No rate records found for {rate_date}"
        )

    return data
    