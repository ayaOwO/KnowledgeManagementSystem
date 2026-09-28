import enum

from pydantic import BaseModel, Field


class Document(BaseModel, extra="forbid"):
    name: str
    type: DocumentType
    contents: str | bytes
    description: str = ""
    tags: list[str] = Field(default=[])


class DocumentType(enum.Enum):
    IMAGE = "image"
    TEXT = "text"
