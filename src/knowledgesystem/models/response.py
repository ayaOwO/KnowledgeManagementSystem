from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: int
    name: str
    description: str
    content_type: str
    content: bytes
    tags: list[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, ser_json_bytes="base64")
