import enum

from pydantic import BaseModel


class Document(BaseModel, extra="forbid"):
    name: str
    type: DocumentType
    object_path: str
    description: str
    tags: list[str]


class DocumentType(enum.Enum):
    IMAGE = "image"
    TEXT = "text"
