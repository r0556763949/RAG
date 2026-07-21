from llama_index.llms.openai import OpenAI
from agent.extraction.schema import ExtractedKnowledge
from llama_index.core import PromptTemplate
import json
from agent.config import OPENAI_API_KEY
from netfree_unstrict_ssl import unstrict_ssl

unstrict_ssl()


llm = OpenAI(
    model="gpt-4.1-mini",
    api_key=OPENAI_API_KEY,
)
def extract_from_markdown(content: str) -> ExtractedKnowledge:

    prompt = PromptTemplate("""
You are a data extraction system.

Extract structured information from this markdown document.

Find:
- technical decisions
- rules or guidelines
- warnings or sensitive areas

Return only information that matches the schema.

Document:

{content}
""")

    response = llm.structured_predict(
        ExtractedKnowledge,
        prompt,
        content=content
    )

    return response


def save_knowledge(data: ExtractedKnowledge):

    with open(
        "data/knowledge.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data.model_dump(),
            f,
            indent=2,
            ensure_ascii=False
        )
        
        
if __name__ == "__main__":

    with open(
        "data/kiro/structure.md",
        "r",
        encoding="utf-8"
    ) as f:
        content = f.read()


    result = extract_from_markdown(content)

    save_knowledge(result)

    print("Knowledge saved!")