from typing import Optional

from pydantic import BaseModel


class STasksAdd(BaseModel):
    name: str
    description: Optional[str] = None


class STasks(STasksAdd):
    id: int
