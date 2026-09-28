from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from knowledgesystem.dependencies import get_labeler, get_session
from knowledgesystem.logic import AbstractLabeler
from knowledgesystem.models import DocumentsTable
from knowledgesystem.models.response import DocumentResponse

router = APIRouter(tags=["knowledge"])


@router.post("/uploadform", status_code=status.HTTP_201_CREATED)
async def upload_form(
    name: Annotated[str, Form()],
    file_upload: Annotated[UploadFile, File()],
    session: Annotated[AsyncSession, Depends(get_session)],
    labeler: Annotated[AbstractLabeler, Depends(get_labeler)],
) -> None:
    content = await file_upload.read()
    match file_upload.content_type:
        case "text/plain":
            metadata = await labeler.label_text(content.decode(), name)
        case "image/png" | "image/jpeg" | "image/webp":
            metadata = await labeler.label_image(
                content, file_upload.content_type, name
            )
        case _:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    inset_document = insert(DocumentsTable).values(
        name=name,
        content=content,
        content_type=file_upload.content_type,
        tags=metadata.tags,
        description=metadata.description,
    )
    await session.execute(inset_document)
    await session.commit()


@router.get("/search", response_model=list[DocumentResponse])
async def search(
    term: str, session: Annotated[AsyncSession, Depends(get_session)]
) -> list[DocumentResponse]:
    search_query = select(DocumentsTable).where(DocumentsTable.tags.contains([term]))
    res = await session.execute(search_query)
    return [DocumentResponse.model_validate(doc) for doc in res.scalars()]


@router.get("/view", response_model=DocumentResponse)
async def view(
    item_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocumentResponse:
    doc = await session.get(DocumentsTable, item_id)
    return DocumentResponse.model_validate(doc)


@router.get("/list", response_model=list[DocumentResponse])
async def list_items(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[DocumentResponse]:
    documents_list_query = select(DocumentsTable)
    res = await session.execute(documents_list_query)
    return [DocumentResponse.model_validate(doc) for doc in res.scalars()]
