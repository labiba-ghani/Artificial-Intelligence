
from pathlib import Path

from services.pdf_service import extract_pdf_text
from services.text_service import create_text_chunks
from services.rag_service import DocumentRetriever


pdf_path = Path("MySQL Handbook.pdf")

if not pdf_path.exists():
    print(
        "Place MySQL Handbook.pdf in the SmartStudy "
        "folder before running this test."
    )

else:
    pdf_bytes = pdf_path.read_bytes()

    pdf_data = extract_pdf_text(pdf_bytes)

    chunks = create_text_chunks(pdf_data["pages"])

    retriever = DocumentRetriever(chunks)

    questions = [
        "What is a primary key?",
        "What is database normalization?",
        "Explain foreign keys.",
        "What is the capital of France?"
    ]

    for question in questions:

        print(f"\nQuestion: {question}")

        results = retriever.search(
            question=question,
            top_k=3,
            min_score=0.15
        )

        if not results:
            print("No relevant chunks found.")
            continue

        for result in results:
            print(
                f"Page {result['page_number']} | "
                f"Score: {result['score']:.4f}"
            )

            print(result["text"][:250])
            print("-" * 40)

    print("\nChecking for normalization terminology:")

    matching_pages = []

    for page in pdf_data["pages"]:
        text = page["text"].lower()

        if "normalization" in text or "normalisation" in text:
            matching_pages.append(page["page_number"])

    print("Pages containing normalization terms:", matching_pages)
