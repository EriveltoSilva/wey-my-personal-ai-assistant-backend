from typing import Literal, Optional

from pydantic import BaseModel, Field

from src.users.enums import UserRoleEnum


class AuthUser(BaseModel):
    model_config = {"extra": "forbid"}

    id: str
    username: str
    role: UserRoleEnum
    full_name: str


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(10, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
