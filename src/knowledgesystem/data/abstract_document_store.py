from abc import ABC, abstractmethod

from knowledgesystem.models.response import Document, DocumentCreate


class AbstractDocumentStore(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def add_document(self, document: DocumentCreate) -> None:
        pass

    @abstractmethod
    async def delete_document(self, document_id: int) -> None:
        pass

    @abstractmethod
    async def get_all_documents(self) -> list[Document]:
        pass

    @abstractmethod
    async def get_document_by_id(self, document_id: int) -> Document:
        pass

    @abstractmethod
    async def search_documents(self, term: str) -> list[Document]:
        pass
