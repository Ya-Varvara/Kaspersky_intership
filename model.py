from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class Size(BaseModel):
    value: int
    operator: str

    @validator('operator')
    def validate_operator(cls, v):
        if v in ["eq", "gt", "lt", "ge", "le"]:
            return v
        raise ValueError(f"Incorrect operator, should be one of eq, gt, lt, ge, le, not {v}")


class CreationTime(BaseModel):
    value: str
    operator: str

    @validator('value')
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            raise ValueError(f"Incorrect date format, should be RFC 3339, section 5.6 (YYYY-mm-ddTHH:MM:SSZ), not {v}")
        return v

    @validator('operator')
    def validate_operator(cls, v):
        if v in ["eq", "gt", "lt", "ge", "le"]:
            return v
        raise ValueError(f"Incorrect operator, should be one of eq, gt, lt, ge, le, not {v}")

class Search(BaseModel):
    text: Optional[str]
    file_mask: Optional[str]
    size: Optional[Size]
    creation_time: Optional[CreationTime]

    def __setattr__(self, key, value):
        self.__dict__[key] = value
