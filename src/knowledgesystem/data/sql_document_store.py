from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from knowledgesystem.data import AbstractDocumentStore
from knowledgesystem.models import DocumentsTable
from knowledgesystem.models.response import Document, DocumentCreate


class SqlDocumentStore(AbstractDocumentStore):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__()
        self.session_maker = session_maker

    async def add_document(self, document: DocumentCreate) -> None:
        content_text = ""
        if document.content_type == "text/plain":
            content_text = document.content.decode()
        async with self.session_maker() as session:
            insert_document = insert(DocumentsTable).values(
                name=document.name,
                content=document.content,
                content_type=document.content_type,
                tags=document.tags,
                content_text=content_text,
                description=document.description,
            )
            await session.execute(insert_document)
            await session.commit()

    async def delete_document(self, document_id: int) -> None:
        delete_query = delete(DocumentsTable).where(DocumentsTable.id == document_id)
        async with self.session_maker() as session:
            await session.execute(delete_query)
            await session.commit()

    async def get_all_documents(self) -> list[Document]:
        documents_list_query = select(DocumentsTable)
        async with self.session_maker() as session:
            res = await session.execute(documents_list_query)
        return [Document.model_validate(doc) for doc in res.scalars()]

    async def get_document_by_id(self, document_id: int) -> Document:
        async with self.session_maker() as session:
            doc = await session.get(DocumentsTable, document_id)
        return Document.model_validate(doc)

    async def search_documents(self, term: str) -> list[Document]:
        search_query = select(DocumentsTable).where(
            DocumentsTable.tags.contains([term.lower()])
        )
        async with self.session_maker() as session:
            res = await session.execute(search_query)

        return [Document.model_validate(doc) for doc in res.scalars()]
