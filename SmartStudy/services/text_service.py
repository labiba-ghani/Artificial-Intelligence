
def create_text_chunks(
    pages: list[dict],
    chunk_size: int = 800,
    overlap: int = 100
) -> list[dict]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    chunks = []
    chunk_id = 1
    step = chunk_size - overlap

    for page in pages:
        text = page["text"].strip()

        if not text:
            continue

        for start in range(0, len(text), step):
            chunk_text = text[start:start + chunk_size]

            if not chunk_text:
                continue

            chunks.append({
                "chunk_id": chunk_id,
                "page_number": page["page_number"],
                "text": chunk_text
            })

            chunk_id += 1

            if start + chunk_size >= len(text):
                break

    return chunks
