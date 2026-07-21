def route_question(question: str) -> str:

    question_lower = question.lower()

    structured_keywords = [
            "rule",
            "rules",
            "decision",
            "decisions",
            "warning",
            "warnings",
            "avoid",
            "don't change",
            "do not change",
            "sensitive",
            "constraint"
        ]

    for keyword in structured_keywords:
        if keyword in question_lower:
            return "structured"

    return "semantic"