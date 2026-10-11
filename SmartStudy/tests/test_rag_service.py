
from services.rag_service import DocumentRetriever


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

results = retriever.search(
    question=question,
    top_k=2,
    min_score=0.15
)


print(f"\nQuestion: {question}")

print("\nRetrieved document chunks:\n")

for result in results:

    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Page: {result['page_number']}")
    print(f"Similarity: {result['score']:.4f}")
    print(f"Text: {result['text']}")
    print("-" * 50)
