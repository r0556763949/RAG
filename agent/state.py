from dataclasses import dataclass


@dataclass
class AgentState:
    question: str = ""
    route: str = ""
    nodes: list = None
    structured_data: dict = None
    answer: str = ""