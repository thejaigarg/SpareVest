# backend/app/schemas/base.py
from pydantic import BaseModel

class OrmModel(BaseModel):
    # tell Pydantic v2 to pull attributes off ORM objects
    model_config = {"from_attributes": True}
