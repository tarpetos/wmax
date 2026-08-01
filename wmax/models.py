from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    weight: float = Field(..., ge=1, le=500, description="Weight lifted")
    reps: int = Field(..., ge=1, le=100, description="Repetitions performed")
    mode: int = Field(
        1, ge=0, le=2, description="Mode: 0=Power, 1=Average, 2=Endurance"
    )


class CalculateResponse(BaseModel):
    maximum: float
    weight: float
    reps: int
    mode: int
