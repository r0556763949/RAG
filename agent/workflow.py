from llama_index.core.workflow import (
    Workflow,
    step,
    StartEvent,
    StopEvent,
    Context,
)

from agent.events import (
    QuestionValidatedEvent,
    RetrievedNodesEvent,
)

from agent.retriever import retrieve
from agent.synthesizer import response_synthesizer
from agent.state import AgentState


class RAGWorkflow(Workflow):
    @step
    async def validate_question(
        self,
        ctx: Context,
        ev: StartEvent,
    ) -> QuestionValidatedEvent | StopEvent:

        question = ev.question

        if not question.strip():
            return StopEvent(result="Please enter a question.")

        state = AgentState()
        state.question = question

        await ctx.store.set("state", state)
        return QuestionValidatedEvent(question=question)

    @step
    async def retrieve_documents(
        self,
        ctx: Context,
        ev: QuestionValidatedEvent,
    ) -> RetrievedNodesEvent | StopEvent:
        state = await ctx.store.get("state")
        nodes = retrieve(state.question)

        if not nodes:
            return StopEvent(result="No relevant information found.")
        state.nodes = nodes
        await ctx.store.set("state", state)
        return RetrievedNodesEvent(question=state.question, nodes=nodes)

    @step
    async def generate_answer(
        self,
        ctx: Context,
        ev: RetrievedNodesEvent,
    ) -> StopEvent:
        state = await ctx.store.get("state")
        answer = response_synthesizer.synthesize(
            query=state.question,
            nodes=state.nodes,
        )
        state.answer = str(answer)
        await ctx.store.set("state", state)
        return StopEvent(result=state.answer)

    pass
