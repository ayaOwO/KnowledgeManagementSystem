from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from knowledgesystem.dependencies import get_labeler
from knowledgesystem.logic import abstract_labeler
from knowledgesystem.models import Document, DocumentType

router = APIRouter(tags=["knowledge"])
db: list[Document] = []


@router.post("/uploadform", status_code=status.HTTP_201_CREATED)
async def upload_form(
    name: Annotated[str, Form()],
    file_upload: Annotated[UploadFile, File()],
    labeler: Annotated[abstract_labeler, Depends(get_labeler)],
) -> None:
    content = await file_upload.read()
    document_type = DocumentType.TEXT
    if file_upload.content_type != "text/plain":
        document_type = DocumentType.IMAGE
        metadata = await labeler.label_image(content, file_upload.content_type, name)
    else:
        content = content.decode("utf-8")
        metadata = await labeler.label_text(content, name)

    document = Document(
        name=name,
        type=document_type,
        contents=content,
        tags=metadata.tags,
        description=metadata.description,
    )

    db.append(document)


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
