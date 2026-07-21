from llama_index.core.response_synthesizers import (
    get_response_synthesizer,
)

from agent.llm import llm

response_synthesizer = get_response_synthesizer(
    llm=llm
)