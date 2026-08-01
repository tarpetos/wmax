from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    """
    Модель запроса для расчета одноповторного максимума.

    Attributes:
        weight (float): Поднятый вес.
        reps (int): Количество повторений.
        mode (int): Режим мышечных волокон (0=Сила, 1=Баланс, 2=Выносливость).
    """

    weight: float = Field(..., ge=1, le=500, description="Weight lifted")
    reps: int = Field(..., ge=1, le=100, description="Repetitions performed")
    mode: int = Field(
        1, ge=0, le=2, description="Mode: 0=Power, 1=Average, 2=Endurance"
    )


class CalculateResponse(BaseModel):
    """
    Модель ответа с результатом расчета одноповторного максимума.

    Attributes:
        maximum (float): Рассчитанный 1ПМ.
        weight (float): Поднятый вес.
        reps (int): Количество повторений.
        mode (int): Использованный режим.
    """

    maximum: float
    weight: float
    reps: int
    mode: int
