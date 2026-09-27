from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from knowledgesystem.logic import AbstractLabeler, AiLabeler
from knowledgesystem.models import Settings


@lru_cache
def get_settings():
    return Settings()


def get_labeler(
    settings: Annotated[Settings, Depends(get_settings)],
) -> AbstractLabeler:
    return AiLabeler(settings)
