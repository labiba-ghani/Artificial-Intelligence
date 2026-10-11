

from services.rag_service import DocumentRetriever
from services.rag_answer_service import answer_from_document


sample_chunks = [
    {
        "chunk_id": 1,
        "page_number": 2,
        "text": (
            "A primary key uniquely identifies "
            "each record in a database table."
        )
    },
    {
        "chunk_id": 2,
        "page_number": 5,
        "text": (
            "A foreign key establishes a relationship "
            "between two database tables."
        )
    },
    {
        "chunk_id": 3,
        "page_number": 8,
        "text": (
            "Database normalization reduces "
            "data redundancy."
        )
    }
]


retriever = DocumentRetriever(sample_chunks)

question = "What is a primary key?"


for provider in ["groq", "ollama"]:

    print(f"\n========== {provider.upper()} ==========")

    result = answer_from_document(
        question=question,
        retriever=retriever,
        provider=provider
    )

    print("\nAnswer:")
    print(result["answer"])

    print("\nRetrieved sources:")

    for source in result["sources"]:
        print(
            f"Page {source['page_number']} | "
            f"Chunk {source['chunk_id']} | "
            f"Score: {source['score']:.4f}"
        )
