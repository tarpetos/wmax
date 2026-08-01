from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    """
    Request model for calculating the one-repetition maximum.

    Attributes:
        weight (float): Lifted weight.
        reps (int): Number of repetitions.
        mode (int): Muscle fiber mode (0=Power, 1=Average, 2=Endurance).
    """

    weight: float = Field(..., ge=1, le=500, description="Weight lifted")
    reps: int = Field(..., ge=1, le=100, description="Repetitions performed")
    mode: int = Field(1, ge=0, le=2, description="Mode: 0=Power, 1=Average, 2=Endurance")
    unit: str = Field("kg", description="Unit: kg or lbs")


class CalculateResponse(BaseModel):
    """
    Response model with the result of the one-repetition maximum calculation.

    Attributes:
        maximum (float): Calculated 1RM in primary unit.
        maximum_alt (float): Calculated 1RM in alternative unit.
        weight (float): Lifted weight.
        reps (int): Number of repetitions.
        mode (int): Used mode.
    """

    maximum: float
    maximum_alt: float
    weight: float
    reps: int
    mode: int
    unit: str
