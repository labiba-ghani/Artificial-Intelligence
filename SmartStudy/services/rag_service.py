
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentRetriever:

    def __init__(self, chunks: list[dict]):

        # Keep only chunks containing readable text
        self.chunks = [
            chunk
            for chunk in chunks
            if chunk["text"].strip()
        ]

        if not self.chunks:
            raise ValueError(
                "No readable document chunks available."
            )

        # Extract text from each chunk
        texts = [
            chunk["text"]
            for chunk in self.chunks
        ]

        # Initialize the TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        # Convert document chunks into TF-IDF vectors
        self.document_vectors = (
            self.vectorizer.fit_transform(texts)
        )

    # --------------------------------------------------
    # Extract Meaningful Keywords from Question
    # --------------------------------------------------

    def _get_query_keywords(
        self,
        question: str
    ) -> set[str]:

        analyzer = self.vectorizer.build_analyzer()

        keywords = set(analyzer(question))

        # Remove general instruction words
        question_words = {
            "explain",
            "describe",
            "define",
            "tell",
            "give",
            "example",
            "examples",
            "difference",
            "discuss",
            "meaning"
        }

        return keywords - question_words

    # --------------------------------------------------
    # Search Relevant Document Chunks
    # --------------------------------------------------

    def search(
        self,
        question: str,
        top_k: int = 3,
        min_score: float = 0.15
    ) -> list[dict]:

        # Check for an empty question
        if not question.strip():
            return []

        # Check for an invalid number of results
        if top_k <= 0:
            return []

        # Convert the question into a TF-IDF vector
        question_vector = self.vectorizer.transform(
            [question]
        )

        # Extract meaningful keywords from the question
        query_keywords = self._get_query_keywords(
            question
        )

        # No meaningful keywords available
        if not query_keywords:
            return []

        # Calculate similarity between the question
        # and all document chunks
        similarities = cosine_similarity(
            question_vector,
            self.document_vectors
        )[0]

        # Sort chunk indexes by similarity (highest first)
        ranked_indexes = similarities.argsort()[::-1]

        results = []

        # Examine chunks in order of similarity
        for index in ranked_indexes:

            score = float(similarities[index])

            # Skip chunks below the similarity threshold
            if score < min_score:
                continue

            chunk = self.chunks[index]

            # Extract keywords from the current chunk
            chunk_keywords = set(
                self.vectorizer.build_analyzer()(
                    chunk["text"]
                )
            )

            # Calculate keyword coverage
            keyword_coverage = (
                len(query_keywords & chunk_keywords)
                / len(query_keywords)
            )

            # Skip chunks with insufficient keyword coverage
            if keyword_coverage < 0.75:
                continue

            # Store the relevant chunk
            results.append({
                "chunk_id": chunk["chunk_id"],
                "page_number": chunk["page_number"],
                "text": chunk["text"],
                "score": score
            })

            # Stop after collecting enough valid chunks
            if len(results) >= top_k:
                break

        return results
