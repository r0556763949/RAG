from pinecone import Pinecone

from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.postprocessor import SimilarityPostprocessor

from netfree_unstrict_ssl import unstrict_ssl
unstrict_ssl()

from agent.config import (
    COHERE_API_KEY,
    PINECONE_API_KEY,
)

#COHERE
embed_model = CohereEmbedding(
    api_key=COHERE_API_KEY,
    model_name="embed-english-v3.0",
    input_type="search_document",
)

#PINECONE
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("rag-agent-memory")

#vectors in pinecone
vector_store = PineconeVectorStore(
    pinecone_index=index
)

vector_index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    embed_model=embed_model,
)

#withdrawl
retriever = vector_index.as_retriever(
    similarity_top_k=3
)
#only more than 0.3
postprocessor = SimilarityPostprocessor(
    similarity_cutoff=0.3
)
#the function that retrieves the answer from the vector store
def retrieve(question: str):
    
        results = retriever.retrieve(question)

        filtered = postprocessor.postprocess_nodes(
            results,
            query_str=question
        )

        return filtered