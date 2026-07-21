import json


def retrieve_structured(question: str):

    with open(
        "data/knowledge.json",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    question_lower = question.lower()

    if "rule" in question_lower:
        return data["rules"]

    if "decision" in question_lower:
        return data["decisions"]

    if "warning" in question_lower:
        return data["warnings"]

    return []