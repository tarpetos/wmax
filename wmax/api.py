import logging

from fastapi import APIRouter, HTTPException

from wmax.core import calculate_1rm
from wmax.models import CalculateRequest, CalculateResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api")


@router.post("/calculate", response_model=CalculateResponse)
def calculate(request: CalculateRequest) -> CalculateResponse:
    """
    Эндпоинт для расчета одноповторного максимума.

    Args:
        request (CalculateRequest): Запрос с весом, повторениями и режимом.

    Returns:
        CalculateResponse: Ответ с рассчитанным максимумом.

    Raises:
        HTTPException: Если данные для расчета некорректны.
    """
    logger.info("Получен запрос на расчет 1ПМ: %s", request)
    try:
        maximum = calculate_1rm(
            weight=request.weight, reps=request.reps, mode=request.mode
        )
        logger.info("Успешно рассчитан результат: %s", maximum)
        return CalculateResponse(
            maximum=maximum,
            weight=request.weight,
            reps=request.reps,
            mode=request.mode,
        )
    except ValueError as e:
        logger.warning("Ошибка проверки данных: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
