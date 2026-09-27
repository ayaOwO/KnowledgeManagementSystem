from abc import ABC, abstractmethod

from knowledgesystem.models import Document


class AbstractLabeler(ABC):
    @abstractmethod
    async def label(self, document: Document) -> Document:
        pass
