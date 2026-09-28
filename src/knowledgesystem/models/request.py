from pydantic import BaseModel


class GeneratedMetadata(BaseModel):
    description: str
    tags: list[str]
