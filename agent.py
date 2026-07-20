from llama_index.core import SimpleDirectoryReader
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.node_parser import SentenceSplitter
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.response_synthesizers import get_response_synthesizer
import os
from dotenv import load_dotenv
from netfree_unstrict_ssl import unstrict_ssl
unstrict_ssl()
load_dotenv()

#COHERE
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
from llama_index.embeddings.cohere import CohereEmbedding

embed_model = CohereEmbedding(
    api_key=COHERE_API_KEY,
    model_name="embed-english-v3.0",
    input_type="search_document",
)

#PINECONE
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)

pinecone_index = pc.Index("rag-agent-memory")

vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index
)
storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)
#OPENAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = OpenAI(
    model="gpt-4.1-mini",
    api_key=OPENAI_API_KEY,
)

index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    embed_model=embed_model,
)

retriever = index.as_retriever(
    similarity_top_k=3
)

postprocessor = SimilarityPostprocessor(
    similarity_cutoff=0.3
)

query = "What is the project structure?"

results = retriever.retrieve(query)
filtered_results = postprocessor.postprocess_nodes(
    results,
    query_str=query
)

response_synthesizer = get_response_synthesizer(
    llm=llm
)

response = response_synthesizer.synthesize(
    query=query,
    nodes=filtered_results
)


def ask(question):

    results = retriever.retrieve(question)

    filtered_results = postprocessor.postprocess_nodes(
        results,
        query_str=question
    )

    response = response_synthesizer.synthesize(
        query=question,
        nodes=filtered_results
    )

    return str(response)


