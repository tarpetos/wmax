import logging

logger = logging.getLogger(__name__)

RATES = [
    [1, 2, 3, 4, 6, 8, 10, 12, 18, 26, 30],
    [1, 2, 4, 6, 8, 10, 12, 18, 26, 30, 38],
    [1, 2, 4, 8, 10, 12, 18, 26, 30, 38, 50],
]


def calculate_1rm(weight: float, reps: int, mode: int = 1) -> float:
    """
    Рассчитывает одноповторный максимум (1ПМ).

    Args:
        weight (float): Поднятый вес в килограммах.
        reps (int): Количество повторений.
        mode (int): Режим мышечных волокон (0 = Сила, 1 = Баланс, 2 = Выносливость).

    Returns:
        float: Рассчитанный 1ПМ.

    Raises:
        ValueError: Если входные данные некорректны.
    """
    logger.debug(
        "Расчет 1ПМ начат: вес=%s, повторения=%s, режим=%s", weight, reps, mode
    )
    if weight < 1 or weight > 500:
        logger.error("Указан неверный вес: %s", weight)
        raise ValueError("Weight must be between 1 and 500 kg")
    if reps < 1 or reps > 100:
        logger.error("Указано неверное количество повторений: %s", reps)
        raise ValueError("Reps must be between 1 and 100")
    if mode not in (0, 1, 2):
        logger.error("Указан неверный режим: %s", mode)
        raise ValueError("Mode must be 0 (Power), 1 (Average), or 2 (Endurance)")

    mode_rates = RATES[mode]
    found_i = len(mode_rates)
    for i, rate in enumerate(mode_rates):
        if rate > reps:
            found_i = i
            break

    percent = 100 - (found_i - 1) * 5

    maximum = round(weight / (percent / 100.0))
    logger.info("Расчет завершен. Максимум: %s", maximum)
    return float(maximum)
