from typing import Annotated

from fastapi import APIRouter, Depends, Form, status

from knowledgesystem.dependencies import get_labeler
from knowledgesystem.logic import abstract_labeler
from knowledgesystem.models import Document

router = APIRouter(tags=["knowledge"])
db: list[Document] = []


@router.post("/uploadform", status_code=status.HTTP_201_CREATED)
async def upload_form(
    document: Annotated[Document, Form()],
    labeler: Annotated[abstract_labeler, Depends(get_labeler)],
) -> None:
    db.append(labeler.label(document))


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(
    document: Document,
    labeler: Annotated[abstract_labeler, Depends(get_labeler)],
) -> None:
    db.append(labeler.label(document))


@router.get("/search", response_model=list[Document])
async def search(
    term: str,
) -> list[Document]:
    return [document for document in db if term.lower() in document.description.lower()]


@router.get("/view", response_model=Document)
async def view(item_id: int) -> Document:
    return db[item_id]


@router.get("/list", response_model=list[Document])
async def list_items() -> list[Document]:
    return db
