from llama_index.llms.openai import OpenAI
from netfree_unstrict_ssl import unstrict_ssl
unstrict_ssl()
from agent.config import OPENAI_API_KEY

llm = OpenAI(
    model="gpt-4.1-mini",
    api_key=OPENAI_API_KEY,
)