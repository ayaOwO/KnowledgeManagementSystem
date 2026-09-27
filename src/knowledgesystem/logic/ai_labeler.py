from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from knowledgesystem.logic import abstract_labeler
from knowledgesystem.models import Document, Settings


class AiLabeler(abstract_labeler.AbstractLabeler):
    def __init__(self, settings: Settings):
        model = OpenAIChatModel(
            settings.openai_model,
            provider=OpenAIProvider(
                base_url=settings.openai_endpoint,
                api_key=settings.openai_api_key,
            ),
        )

        self.agent: Agent = Agent(model)

    async def label(self, document: Document) -> Document:
        document = document.model_copy()
        res = await self.agent.run(
            document.description, instructions="Read this text", model=list[str]
        )
        document.tags = res.output
        return document
