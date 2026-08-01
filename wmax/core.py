RATES = [
    [1, 2, 3, 4, 6, 8, 10, 12, 18, 26, 30],
    [1, 2, 4, 6, 8, 10, 12, 18, 26, 30, 38],
    [1, 2, 4, 8, 10, 12, 18, 26, 30, 38, 50],
]


def calculate_1rm(weight: float, reps: int, mode: int = 1) -> float:
    """
    Calculate the One Rep Max (1RM) based on weight and reps.
    mode: 0 = Power, 1 = Average, 2 = Endurance
    """
    if weight < 1 or weight > 500:
        raise ValueError("Weight must be between 1 and 500 kg")
    if reps < 1 or reps > 100:
        raise ValueError("Reps must be between 1 and 100")
    if mode not in (0, 1, 2):
        raise ValueError("Mode must be 0 (Power), 1 (Average), or 2 (Endurance)")

    mode_rates = RATES[mode]
    found_i = len(mode_rates)
    for i, rate in enumerate(mode_rates):
        if rate > reps:
            found_i = i
            break

    percent = 100 - (found_i - 1) * 5

    maximum = round(weight / (percent / 100.0))
    return float(maximum)
