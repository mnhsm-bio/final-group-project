from typing import Optional
from pydantic import BaseModel


class Resource_ManagementBase(BaseModel):
    resource_amount: int
    unit: str


class Resource_ManagementCreate(Resource_ManagementBase):
    pass


class Resource_ManagementUpdate(BaseModel):
    resource_amount: Optional[int] = None
    unit: Optional[str] = None


class Resource_Management(Resource_ManagementBase):
    id: int

    class ConfigDict:
        from_attributes = True