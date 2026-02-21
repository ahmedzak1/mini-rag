from pydantic import BaseModel, field, validator
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    _id: Optional[ObjectId] 
    project_id: str = Filed(..., min_length=1)

    @validator('project_id')
    def validate_project_id(cls, v):
        if not v.isnumeric():
            raise ValueError('project_id must be a numeric string')

        return v

    class Config:
        arbitrary_types_allowed = True
        