from pydantic import BaseModel, Field, root_validator
from wmax.core import get_weight_limits

class CalculateRequest(BaseModel):
    weight: float = Field(..., description="Weight lifted")
    reps: int = Field(..., ge=1, le=100, description="Repetitions performed")
    mode: int = Field(1, ge=0, le=2, description="Mode: 0=Power, 1=Average, 2=Endurance")
    unit: str = Field("kg", description="Unit: kg or lbs")

    @root_validator(pre=False)
    def validate_weight(cls, values):
        unit = values.get("unit")
        weight = values.get("weight")
        if unit and weight is not None:
            min_w, max_w = get_weight_limits(unit)
            if weight < min_w or weight > max_w:
                raise ValueError(f"Weight must be between {min_w:.1f} and {max_w:.1f} {unit}")
        return values

class CalculateResponse(BaseModel):
    maximum: float = Field(..., description="Calculated 1RM in the requested unit")
    maximum_alt: float = Field(..., description="Calculated 1RM in the alternative unit")
    weight: float = Field(..., description="The weight provided")
    reps: int = Field(..., description="The reps provided")
    mode: int = Field(..., description="The mode provided")
    unit: str = Field(..., description="The unit provided")
