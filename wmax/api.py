from fastapi import APIRouter, HTTPException
from loguru import logger

from wmax.core import calculate_1rm
from wmax.models import CalculateRequest, CalculateResponse

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
    logger.info("Received request for 1RM calculation: {}", request)
    try:
        maximum = calculate_1rm(weight=request.weight, reps=request.reps, mode=request.mode)
        logger.info("Successfully calculated result: {}", maximum)
        return CalculateResponse(
            maximum=maximum,
            weight=request.weight,
            reps=request.reps,
            mode=request.mode,
        )
    except ValueError as e:
        logger.warning("Data validation error: {}", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
