import logging

from fastapi import APIRouter, HTTPException

from wmax.core import calculate_1rm
from wmax.models import CalculateRequest, CalculateResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api")


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
    logger.info("Received request for 1RM calculation: %s", request)
    try:
        maximum = calculate_1rm(weight=request.weight, reps=request.reps, mode=request.mode)
        logger.info("Successfully calculated result: %s", maximum)
        return CalculateResponse(
            maximum=maximum,
            weight=request.weight,
            reps=request.reps,
            mode=request.mode,
        )
    except ValueError as e:
        logger.warning("Data validation error: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
