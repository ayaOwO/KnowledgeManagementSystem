from collections.abc import AsyncIterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from knowledgesystem.logic import AbstractLabeler, AiLabeler
from knowledgesystem.models import Settings


@lru_cache
def get_settings():
    return Settings()


def get_labeler(
    settings: Annotated[Settings, Depends(get_settings)],
) -> AbstractLabeler:
    return AiLabeler(settings)


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with request.app.state.session_factory() as session:
        yield session
