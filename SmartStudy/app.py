
import hashlib

import streamlit as st

from agent.smartstudy_agent import run_agent
from services.pdf_service import extract_pdf_text
from services.text_service import create_text_chunks
from services.rag_service import DocumentRetriever
from services.rag_answer_service import answer_from_document


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SmartStudy",
    page_icon="🎓",
    layout="centered"
)


# --------------------------------------------------
# Application Heading
# --------------------------------------------------

st.title("🎓 SmartStudy")

st.write(
    "Your AI-powered personalized learning assistant."
)


# --------------------------------------------------
# AI Provider Selection
# --------------------------------------------------

provider = st.selectbox(
    "Choose your AI provider:",
    ["groq", "ollama"],
    format_func=lambda name: name.capitalize()
)


# --------------------------------------------------
# General AI Assistant
# --------------------------------------------------

st.header("🤖 SmartStudy AI Assistant")

question = st.text_area(
    "What would you like to learn?",
    placeholder="Example: Which topic should I revise first?"
)

if st.button("Ask SmartStudy", type="primary"):

    if not question.strip():
        st.warning("Please enter a question first.")

    else:
        with st.spinner("SmartStudy is thinking..."):

            try:
                answer = run_agent(
                    question=question,
                    provider=provider
                )

                st.session_state["general_answer"] = answer

            except Exception as error:
                st.error(
                    "Something went wrong while processing "
                    "your question."
                )
                st.caption(
                    f"Technical details: {type(error).__name__}"
                )

if "general_answer" in st.session_state:

    st.subheader("SmartStudy's Answer")

    st.markdown(
        st.session_state["general_answer"]
    )


# --------------------------------------------------
# PDF Upload Section
# --------------------------------------------------

st.divider()

st.header("📄 Upload Lecture Notes")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
    help="Upload a text-based PDF containing lecture notes."
)


# --------------------------------------------------
# Process Uploaded PDF
# --------------------------------------------------

if uploaded_file is not None:

    try:
        pdf_bytes = uploaded_file.getvalue()

        # Create a unique fingerprint for the PDF
        file_id = hashlib.sha256(pdf_bytes).hexdigest()

        # Only process when the uploaded PDF changes
        if st.session_state.get("pdf_file_id") != file_id:

            pdf_data = extract_pdf_text(pdf_bytes)

            if pdf_data["has_text"]:

                chunks = create_text_chunks(
                    pdf_data["pages"]
                )

                retriever = DocumentRetriever(chunks)

            else:
                chunks = []
                retriever = None

            # Save processed data for future interactions
            st.session_state["pdf_data"] = pdf_data
            st.session_state["pdf_chunks"] = chunks
            st.session_state["pdf_retriever"] = retriever
            st.session_state["pdf_file_id"] = file_id

            # Clear the previous document's answer
            st.session_state.pop(
                "document_result", None
            )

        # Load the processed document
        pdf_data = st.session_state["pdf_data"]
        chunks = st.session_state["pdf_chunks"]
        retriever = st.session_state["pdf_retriever"]

        st.success(
            f"PDF processed successfully! "
            f"Total pages: {pdf_data['page_count']}"
        )

        # ------------------------------------------
        # Display Document Information
        # ------------------------------------------

        if pdf_data["has_text"]:

            st.info(
                f"Created {len(chunks)} text chunks "
                f"for RAG processing."
            )

            st.write(
                f"Extracted characters: "
                f"{len(pdf_data['full_text'])}"
            )

            # --------------------------------------
            # Preview Text Chunks
            # --------------------------------------

            with st.expander("Preview text chunks"):

                for chunk in chunks[:5]:

                    st.write(
                        f"Chunk {chunk['chunk_id']} "
                        f"— Page {chunk['page_number']}"
                    )

                    st.text(chunk["text"])

                    st.divider()

            # --------------------------------------
            # Preview Full Extracted Text
            # --------------------------------------

            with st.expander("View extracted text"):

                st.text_area(
                    "Document content",
                    value=pdf_data["full_text"],
                    height=300,
                    disabled=True
                )

            # --------------------------------------
            # RAG Question Answering
            # --------------------------------------

            st.divider()

            st.subheader(
                "🤖 Ask Questions About Your PDF"
            )

            document_question = st.text_area(
                "Enter your question about the uploaded notes:",
                placeholder=(
                    "Example: Explain primary keys "
                    "according to these notes."
                ),
                key="document_question"
            )

            if st.button(
                "Ask About Document",
                type="primary"
            ):

                if not document_question.strip():

                    st.warning(
                        "Please enter a question."
                    )

                else:

                    with st.spinner(
                        "Searching lecture notes and "
                        "generating an answer..."
                    ):

                        result = answer_from_document(
                            question=document_question,
                            retriever=retriever,
                            provider=provider
                        )

                        # Save answer between reruns
                        st.session_state[
                            "document_result"
                        ] = result

            # --------------------------------------
            # Display RAG Answer
            # --------------------------------------

            if "document_result" in st.session_state:

                result = st.session_state[
                    "document_result"
                ]

                st.subheader("Answer")

                st.markdown(
                    result["answer"]
                )

                # ----------------------------------
                # Display Retrieved Sources
                # ----------------------------------

                if result["sources"]:

                    with st.expander(
                        "📚 View Retrieved Sources"
                    ):

                        for source in result["sources"]:

                            st.write(
                                f"**Page {source['page_number']}** "
                                f"— Chunk {source['chunk_id']}"
                            )

                            st.caption(
                                f"Similarity: "
                                f"{source['score']:.4f}"
                            )

                            # Find original chunk text
                            matching_chunk = next(
                                (
                                    chunk
                                    for chunk in chunks
                                    if chunk["chunk_id"]
                                    == source["chunk_id"]
                                ),
                                None
                            )

                            if matching_chunk:

                                st.text(
                                    matching_chunk["text"]
                                )

                            st.divider()

        else:

            st.warning(
                "No readable text was found in this PDF. "
                "It may contain scanned images instead "
                "of selectable text."
            )

    except ValueError as error:

        st.warning(str(error))

    except Exception as error:

        st.error(
            "Unable to process the document "
            "or generate an answer."
        )

        st.caption(
            f"Error type: {type(error).__name__}"
        )

else:

    # Clear stored document data if upload is removed
    for key in [
        "pdf_file_id",
        "pdf_data",
        "pdf_chunks",
        "pdf_retriever",
        "document_result"
    ]:
        st.session_state.pop(key, None)


