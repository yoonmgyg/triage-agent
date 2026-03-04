import json
from uuid import uuid4

import httpx
from a2a.client import (
    A2ACardResolver,
    ClientConfig,
    ClientFactory,
)
from a2a.types import (
    Message,
    Part,
    Role,
    TextPart,
    DataPart,
)

DEFAULT_TIMEOUT = 300

def create_message(
    *, role: Role = Role.user, text: str, context_id: str | None = None
) -> Message:
    return Message(
        kind="message",
        role=role,
        parts=[Part(TextPart(kind="text", text=text))],
        message_id=uuid4().hex,
        context_id=context_id,
    )

def merge_parts(parts: list[Part]) -> str:
    chunks = []
    for part in parts:
        if isinstance(part.root, TextPart):
            chunks.append(part.root.text)
        elif isinstance(part.root, DataPart):
            chunks.append(json.dumps(part.root.data, indent=2))
    return "\n".join(chunks)

class Messenger:
    def __init__(self):
        self._context_ids = {}
        self._httpx_client = None
        self._clients = {}

    async def _get_client(self, url: str):
        if self._httpx_client is None:
            self._httpx_client = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)
        
        if url not in self._clients:
            resolver = A2ACardResolver(httpx_client=self._httpx_client, base_url=url)
            agent_card = await resolver.get_agent_card()
            config = ClientConfig(httpx_client=self._httpx_client, streaming=False)
            factory = ClientFactory(config)
            self._clients[url] = factory.create(agent_card)
        
        return self._clients[url]

    async def talk_to_agent(
        self,
        message: str,
        url: str,
        new_conversation: bool = False,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """
        Communicate with another agent by sending a message and receiving their response.
        """
        client = await self._get_client(url)
        context_id = None if new_conversation else self._context_ids.get(url, None)
        outbound_msg = create_message(text=message, context_id=context_id)
        
        outputs = {"response": "", "context_id": None, "status": "completed"}

        async for event in client.send_message(outbound_msg):
            match event:
                case Message() as msg:
                    outputs["context_id"] = msg.context_id
                    outputs["response"] += merge_parts(msg.parts)
                
                case (task, update):
                    outputs["context_id"] = task.context_id
                    outputs["status"] = task.status.state.value
                    if update and update.message:
                        outputs["response"] += merge_parts(update.message.parts)
                    if task.status.message:
                        outputs["response"] += merge_parts(task.status.message.parts)
                    if task.artifacts:
                        for artifact in task.artifacts:
                            outputs["response"] += merge_parts(artifact.parts)

                case _ if hasattr(event, "artifact"): # ArtifactUpdate
                    outputs["response"] += merge_parts(event.artifact.parts)

        if outputs.get("status", "completed") != "completed":
            raise RuntimeError(f"{url} responded with: {outputs}")
        self._context_ids[url] = outputs.get("context_id", None)
        return outputs["response"]

    def reset(self):
        self._context_ids = {}

    async def close(self):
        if self._httpx_client:
            await self._httpx_client.aclose()
            self._httpx_client = None
            self._clients = {}
