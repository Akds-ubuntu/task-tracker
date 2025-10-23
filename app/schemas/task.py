from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class TaskCreate(BaseModel):
    title: str
    start_dt: datetime
    end_dt: Optional[datetime] = None
    description: Optional[str] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_dt and self.end_dt < self.start_dt:
            raise ValueError("Дата окончания не может быть раньше даты начала")
        return self


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_dt: Optional[datetime] = None
    end_dt: Optional[datetime] = None
    is_done: Optional[bool] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_dt and self.end_dt and self.end_dt < self.start_dt:
            raise ValueError("Дата окончания не может быть раньше даты начала")
        return self


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_dt: datetime
    end_dt: Optional[datetime] = None
    is_done: bool

    class Config:
        from_attributes = True
