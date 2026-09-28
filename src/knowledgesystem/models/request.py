from pydantic import BaseModel, Field


class GeneratedMetadata(BaseModel):
    description: str = Field(max_length=255)
    tags: list[str]
