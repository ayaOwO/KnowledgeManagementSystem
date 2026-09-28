import contextlib
from pathlib import Path

import logfire
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.responses import HTMLResponse

from .dependencies import get_settings
from .routers import knowledge_store


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine = create_async_engine(settings.database_url)
    app.state.session_factory = async_sessionmaker(engine, expire_on_commit=False)
    yield
    await app.state.engine.dispose()


app = FastAPI(lifespan=lifespan)

logfire.configure()
logfire.instrument_pydantic_ai()
logfire.instrument_fastapi(app)

app.include_router(knowledge_store.router)


@app.get("/")
async def root():
    return HTMLResponse((Path(__file__).parent / "front" / "index.html").read_text())
