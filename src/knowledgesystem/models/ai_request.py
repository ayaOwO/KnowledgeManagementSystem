from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field


def to_lower(s: list[str]) -> list[str]:
    return [i.lower() for i in s]


class GeneratedMetadata(BaseModel):
    description: str = Field(max_length=500)
    tags: Annotated[list[str], AfterValidator(to_lower)]
