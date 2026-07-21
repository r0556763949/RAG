from llama_index.core.workflow import Event


class QuestionValidatedEvent(Event):
    question: str


class RetrievedNodesEvent(Event):
    question: str
    nodes: list
    
class NoContextEvent(Event):
    reason: str
