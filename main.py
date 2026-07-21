import asyncio
from agent.workflow import RAGWorkflow

async def main():
    workflow = RAGWorkflow(timeout=60)

    result = await workflow.run(
        question="What is the project structure?"
    )

    print(result)

asyncio.run(main())