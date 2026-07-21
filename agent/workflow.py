from llama_index.core.workflow import (
    Workflow,
    step,
    StartEvent,
    StopEvent,
    Context,
)

from agent.llm import llm
from agent.events import (
    QuestionValidatedEvent,
    RetrievedNodesEvent,
     StructuredRouteEvent,
    SemanticRouteEvent,
)

from agent.retriever import retrieve
from agent.synthesizer import response_synthesizer
from agent.state import AgentState
from agent.events import StructuredDataRetrievedEvent
from agent.structured_retriever import retrieve_structured
from agent.router import route_question

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
    async def route(
        self,
        ctx: Context,
        ev: QuestionValidatedEvent,
    ) -> StructuredRouteEvent | SemanticRouteEvent:

        state = await ctx.store.get("state")

        selected_route = route_question(
            state.question
        )

        state.route = selected_route

        await ctx.store.set(
            "state",
            state
        )

        print("ROUTE:", selected_route)

        if selected_route == "structured":

            return StructuredRouteEvent(
                question=state.question
            )

        else:

            return SemanticRouteEvent(
                question=state.question
            )
    
        
    @step
    async def retrieve_structured_data(
        self,
        ctx: Context,
        ev: StructuredRouteEvent,
    ) -> StructuredDataRetrievedEvent | StopEvent:

        state = await ctx.store.get("state")

        data = retrieve_structured(
            state.question
        )


        if not data:
            return StopEvent(
                result="No structured information found."
            )


        state.structured_data = data

        await ctx.store.set(
            "state",
            state
        )

        print("STRUCTURED DATA:", data)


        return StructuredDataRetrievedEvent(
            question=state.question,
            data=data
        )
    @step
    async def retrieve_documents(
        self,
        ctx: Context,
        ev: SemanticRouteEvent,
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
        ev: RetrievedNodesEvent | StructuredDataRetrievedEvent,
    ) -> StopEvent:

        state = await ctx.store.get("state")

        if isinstance(ev, RetrievedNodesEvent):

            answer = response_synthesizer.synthesize(
                query=state.question,
                nodes=state.nodes,
            )

        else:

           answer = llm.complete(
            f"""
            Answer the question using this data:

            {state.structured_data}

            Question:
            {state.question}
            """
        )

        state.answer = str(answer)

        await ctx.store.set(
            "state",
            state
        )

        return StopEvent(
            result=state.answer
        )
    pass
