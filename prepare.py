from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
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

def load_documents():
    reader = SimpleDirectoryReader(
        input_dir="data",
        recursive=True
    )

    documents = reader.load_data()

    print(f"Loaded documents: {len(documents)}")

    return documents


def chunk_documents(documents):

    splitter = SentenceSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    nodes = splitter.get_nodes_from_documents(
        documents,
        show_progress=True
    )

    print(f"Created nodes: {len(nodes)}")

    return nodes


if __name__ == "__main__":
    documents = load_documents()
    nodes = chunk_documents(documents)
    print("Creating VectorStoreIndex...")

    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        embed_model=embed_model,
    )

    # print("Index created successfully!")
    # print("Testing Cohere connection...")

    # embedding = embed_model.get_text_embedding("Hello world")

    # print(f"Embedding created successfully!")
    # print(f"Embedding length: {len(embedding)}")