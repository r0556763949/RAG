from dataclasses import dataclass


@dataclass
class AgentState:
    question: str = ""
    nodes: list = None
    answer: str = ""