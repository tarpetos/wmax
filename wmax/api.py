from fastapi import APIRouter, HTTPException

from wmax.core import calculate_1rm
from wmax.models import CalculateRequest, CalculateResponse

router = APIRouter(prefix="/api")


@router.post("/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest) -> CalculateResponse:
    try:
        maximum = calculate_1rm(
            weight=request.weight, reps=request.reps, mode=request.mode
        )
        return CalculateResponse(
            maximum=maximum,
            weight=request.weight,
            reps=request.reps,
            mode=request.mode,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
