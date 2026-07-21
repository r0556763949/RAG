import gradio as gr
import asyncio

from agent.workflow import RAGWorkflow


async def ask_agent(question):
    workflow = RAGWorkflow(timeout=60)

    result = await workflow.run(
        question=question
    )

    return str(result)


def chat(question):
    return asyncio.run(
        ask_agent(question)
    )


demo = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(
        label="Ask about the project"
    ),
    outputs=gr.Textbox(
        label="Answer"
    ),
    title="RAG Agent Memory"
)


demo.launch()