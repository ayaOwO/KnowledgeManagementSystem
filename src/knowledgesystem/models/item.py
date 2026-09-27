import enum

from pydantic import BaseModel


class Document(BaseModel):
    name: str
    type: DocumentType
    object_path: str
    description: str
    tags: list[str]


class DocumentType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
