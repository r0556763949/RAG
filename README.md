# RAG Agent Memory

An AI-powered Retrieval-Augmented Generation (RAG) system for answering questions about software project documentation.

The system combines semantic search with structured knowledge extraction to provide accurate answers based on the type of user query.

---

## Project Overview

The goal of this project is to build an intelligent agent that can analyze project documentation files (`.md`) and answer questions using different retrieval strategies.

The system supports:

- Semantic retrieval for contextual questions.
- Structured retrieval for list-based, rule-based, and time-sensitive questions.
- Event-driven workflow for managing the agent flow.

---

# Architecture

The agent is built as an event-driven workflow using LlamaIndex Workflow.


User Question
|
v
Question Validation
|
v
Router
|
+----------------------+
| |
v v
Semantic Retrieval Structured Retrieval
(Pinecone) (Extracted JSON)
| |
+----------------------+
|
v
Response Generation
|
v
Answer


---

# Main Features

## 1. Semantic Retrieval

The system uses vector search to find relevant documentation sections.

Technologies:

- LlamaIndex Retriever
- Pinecone Vector Database
- Cohere Embeddings

This retrieval method is used for questions that require understanding of the project context.

Example:


How does the frontend communicate with the server?


---

## 2. Structured Data Extraction

Documentation files are analyzed and converted into structured knowledge.

The extraction process identifies:

- Decisions
- Rules
- Warnings

The extracted information is stored as structured JSON data.

Example:

```json
{
  "rules": [
    {
      "rule": "Use kebab-case for file names",
      "scope": "Entire project"
    }
  ]
}

This allows accurate retrieval for questions where semantic search alone may not provide complete results.

Example:

Give me all project rules
3. Query Routing

A routing layer determines the appropriate retrieval strategy.

The router decides whether the question should use:

Semantic Search

For general understanding questions.

Example:

Explain the project structure
Structured Search

For questions requiring complete extracted information.

Example:

What technical decisions were made?
Event Driven Workflow

The workflow is divided into independent steps.

Each step:

Receives an event as input.
Performs a specific task.
Produces the next event.

Main workflow steps:

Question Validation
Query Routing
Semantic Retrieval / Structured Retrieval
Response Generation

Main events:

QuestionValidatedEvent
SemanticRouteEvent
StructuredRouteEvent
RetrievedNodesEvent
StructuredDataRetrievedEvent
Technologies
Python
LlamaIndex
OpenAI API
Pinecone Vector Database
Cohere Embeddings
Gradio
JSON Structured Storage
Project Structure
RAG-Agent-Memory
│
├── agent
│   ├── workflow.py
│   ├── router.py
│   ├── retriever.py
│   ├── structured_retriever.py
│   ├── extraction
│   │   ├── extractor.py
│   │   └── schema.py
│   ├── events.py
│   └── state.py
│
├── data
│   └── markdown documentation files
│
├── extracted_knowledge.json
│
├── main.py
│
└── requirements.txt
Running the Project

Install dependencies:

pip install -r requirements.txt

Create a .env file:

OPENAI_API_KEY=
COHERE_API_KEY=
PINECONE_API_KEY=

Run the application:

python main.py

The Gradio interface allows users to ask questions and receive answers generated from the documentation.

Future Improvements

Possible future improvements:

Replace keyword routing with an LLM-based router.
Automatically detect documentation changes and update extracted data.
Store structured knowledge in a database.
Add confidence-based routing and validation.
Support additional document formats.
Summary

This project demonstrates a complete RAG pipeline:

Extract knowledge from documentation.
Store information both semantically and structurally.
Route user questions to the correct retrieval method.
Generate accurate answers using an LLM.

The combination of semantic retrieval, structured extraction, and event-driven workflow creates a flexible AI agent capable of answering complex project-related questions.