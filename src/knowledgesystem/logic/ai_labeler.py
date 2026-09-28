from pydantic_ai import Agent, BinaryContent
from pydantic_ai.capabilities import Thinking
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from knowledgesystem.logic import abstract_labeler
from knowledgesystem.models import Settings
from knowledgesystem.models.request import GeneratedMetadata

METADATA_INSTRUCTIONS = (
    "Describe the provided content in one clear sentence"
    "Return specific, lowercase tags for its main topics or visible objects. "
    "Use only details supported by the content; avoid guesses and duplicate tags."
)


class AiLabeler(abstract_labeler.AbstractLabeler):
    def __init__(self, settings: Settings):
        model = OpenAIChatModel(
            settings.openai_model,
            provider=OpenAIProvider(
                base_url=settings.openai_endpoint,
                api_key=settings.openai_api_key,
            ),
        )

        self.agent: Agent = Agent(model, capabilities=[Thinking(effort="low")])

    async def label_image(
        self, contents: bytes, media_type: str, name: str
    ) -> GeneratedMetadata:
        res = await self.agent.run(
            [BinaryContent(data=contents, media_type=media_type)],
            instructions=METADATA_INSTRUCTIONS,
            output_type=GeneratedMetadata,
        )
        return res.output

    async def label_text(self, contents: str, name: str) -> GeneratedMetadata:
        res = await self.agent.run(
            contents,
            instructions=METADATA_INSTRUCTIONS,
            output_type=GeneratedMetadata,
        )
        return res.output
