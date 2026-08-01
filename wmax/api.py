import os
import threading
import time

from fastapi import APIRouter, HTTPException
from loguru import logger

from wmax.core import calculate_1rm
from wmax.models import CalculateRequest, CalculateResponse

router = APIRouter(prefix="/api")


@router.post("/quit")
def quit_app() -> dict[str, str]:
    """
    Terminates the application gracefully.
    """
    logger.info("Shutdown requested via API")

    def exit_delay() -> None:
        time.sleep(0.5)
        os._exit(0)

    threading.Thread(target=exit_delay).start()
    return {"status": "shutting down"}


@router.post("/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest) -> CalculateResponse:
    """
    Endpoint for calculating the one-repetition maximum.

    Args:
        request (CalculateRequest): The request payload containing weight, reps, and mode.

    Returns:
        CalculateResponse: The response containing the calculated maximum.

    Raises:
        HTTPException: If the calculation data is invalid.
    """
    logger.info("Received request for 1RM calculation: {}", request)
    try:
        maximum = calculate_1rm(weight=request.weight, reps=request.reps, mode=request.mode, unit=request.unit)

        if request.unit == "kg":
            alt_unit = "lbs"
            alt_weight = request.weight * 2.20462262
        else:
            alt_unit = "kg"
            alt_weight = request.weight / 2.20462262

        maximum_alt = calculate_1rm(weight=alt_weight, reps=request.reps, mode=request.mode, unit=alt_unit)

        logger.info("Successfully calculated result: {} {}, {} {}", maximum, request.unit, maximum_alt, alt_unit)
        return CalculateResponse(
            maximum=maximum,
            maximum_alt=maximum_alt,
            weight=request.weight,
            reps=request.reps,
            mode=request.mode,
            unit=request.unit,
        )
    except ValueError as e:
        logger.warning("Data validation error: {}", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
