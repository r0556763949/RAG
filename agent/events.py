from llama_index.core.workflow import Event


class QuestionValidatedEvent(Event):
    question: str


class RetrievedNodesEvent(Event):
    question: str
    nodes: list
    
class StructuredDataRetrievedEvent(Event):
    question: str
    data: list
    
class NoContextEvent(Event):
    reason: str
    
class SemanticRouteEvent(Event):
    question: str


class StructuredRouteEvent(Event):
    question: str
