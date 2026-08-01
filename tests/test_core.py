import pytest

from wmax.core import calculate_1rm


def test_calculate_1rm_power() -> None:
    assert calculate_1rm(100, 1, 0) == 100
    assert calculate_1rm(100, 4, 0) == round(100 / 0.85)


def test_calculate_1rm_average() -> None:
    assert calculate_1rm(100, 1, 1) == 100
    assert calculate_1rm(100, 6, 1) == round(100 / 0.85)


def test_calculate_1rm_endurance() -> None:
    assert calculate_1rm(100, 1, 2) == 100
    assert calculate_1rm(100, 8, 2) == round(100 / 0.85)


def test_calculate_1rm_high_reps() -> None:
    assert calculate_1rm(100, 50, 2) == round(100 / 0.50)
    assert calculate_1rm(100, 100, 2) == round(100 / 0.50)


def test_calculate_1rm_invalid() -> None:
    with pytest.raises(ValueError, match="Weight must be between"):
        calculate_1rm(0, 5, 1)
    with pytest.raises(ValueError, match="Weight must be between"):
        calculate_1rm(501, 5, 1)
    with pytest.raises(ValueError, match="Reps must be between"):
        calculate_1rm(100, 0, 1)
    with pytest.raises(ValueError, match="Reps must be between"):
        calculate_1rm(100, 101, 1)
    with pytest.raises(ValueError, match="Mode must be"):
        calculate_1rm(100, 5, -1)
    with pytest.raises(ValueError, match="Mode must be"):
        calculate_1rm(100, 5, 3)
