from pathlib import Path

import logfire
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from .models import Document
from .routers import knowledge_store

app = FastAPI()

logfire.configure()
logfire.instrument_pydantic_ai()

app.include_router(knowledge_store.router)

@app.get("/")
async def root():
    return HTMLResponse((Path(__file__).parent / "front" / "index.html").read_text())


