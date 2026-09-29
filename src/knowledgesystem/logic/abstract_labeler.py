from abc import ABC, abstractmethod

from knowledgesystem.models import GeneratedMetadata


class AbstractLabeler(ABC):
    @abstractmethod
    async def label_image(
        self, contents: bytes, media_type: str, name: str
    ) -> GeneratedMetadata:
        pass

    @abstractmethod
    async def label_text(self, contents: str, name: str) -> GeneratedMetadata:
        pass
