from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentCreate(BaseModel):
    name: str
    description: str
    content_type: str
    content: bytes
    tags: list[str]


class Document(DocumentCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, ser_json_bytes="base64")
