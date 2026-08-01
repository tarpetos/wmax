from loguru import logger

RATES = [
    [1, 2, 3, 4, 6, 8, 10, 12, 18, 26, 30],
    [1, 2, 4, 6, 8, 10, 12, 18, 26, 30, 38],
    [1, 2, 4, 8, 10, 12, 18, 26, 30, 38, 50],
]


def my_round(number: float, unit: str = "kg") -> float:
    """
    Rounds the number according to custom rules:
    - If >= 50kg (or 110lbs), rounds to the nearest 2.5.
    - If < 50kg, rounds to the nearest 1.
    """
    threshold = 50.0 if unit == "kg" else 110.0
    if number >= threshold:
        return 2.5 * round(number / 2.5)
    return 1.0 * round(number / 1.0)


def calculate_1rm(weight: float, reps: int, mode: int = 1, unit: str = "kg") -> float:
    """
    Calculates the One Repetition Maximum (1RM).

    Args:
        weight (float): Lifted weight.
        reps (int): Number of repetitions.
        mode (int): Muscle fiber mode (0 = Power, 1 = Average, 2 = Endurance).
        unit (str): Unit of weight ('kg' or 'lbs').

    Returns:
        float: The calculated 1RM.

    Raises:
        ValueError: If the input data is invalid.
    """
    logger.debug("1RM calculation started: weight={}, reps={}, mode={}, unit={}", weight, reps, mode, unit)
    if weight < 1 or weight > 500:
        raise ValueError("Weight must be between 1 and 500")
    if unit not in ("kg", "lbs"):
        raise ValueError("Unit must be kg or lbs")
    if reps < 1 or reps > 100:
        logger.error("Invalid repetitions provided: {}", reps)
        raise ValueError("Reps must be between 1 and 100")
    if mode not in (0, 1, 2):
        logger.error("Invalid mode provided: {}", mode)
        raise ValueError("Mode must be 0 (Power), 1 (Average), or 2 (Endurance)")

    mode_rates = RATES[mode]
    found_i = len(mode_rates)
    for i, rate in enumerate(mode_rates):
        if rate > reps:
            found_i = i
            break

    percent = 100 - (found_i - 1) * 5

    maximum = my_round(weight / (percent / 100.0), unit)
    logger.info("Calculation complete. Maximum: {}", maximum)
    return maximum
