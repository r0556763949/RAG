from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter


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
    for node in nodes[:3]:
