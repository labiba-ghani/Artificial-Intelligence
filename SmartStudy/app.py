
import streamlit as st

from agent.smartstudy_agent import run_agent
from services.pdf_service import extract_pdf_text
from services.text_service import create_text_chunks


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
# Student Question
# --------------------------------------------------

question = st.text_area(
    "What would you like to learn?",
    placeholder="Example: Which topic should I revise first?"
)


# --------------------------------------------------
# Run SmartStudy Agent
# --------------------------------------------------

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

                st.subheader("SmartStudy's Answer")
                st.markdown(answer)

            except Exception as error:
                st.error(
                    "Something went wrong while processing "
                    "your question."
                )

                st.caption(
                    f"Technical details: {type(error).__name__}"
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

        pdf_data = extract_pdf_text(pdf_bytes)

        st.success(
            f"PDF processed successfully! "
            f"Total pages: {pdf_data['page_count']}"
        )

        # Check whether PDF contains readable text
        if pdf_data["has_text"]:

            # --------------------------------------
            # Create Text Chunks
            # --------------------------------------

            chunks = create_text_chunks(
                pdf_data["pages"]
            )

            st.info(
                f"Created {len(chunks)} text chunks "
                f"for future RAG processing."
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
            # Display Extracted Text Information
            # --------------------------------------

            st.write(
                f"Extracted characters: "
                f"{len(pdf_data['full_text'])}"
            )

            # --------------------------------------
            # Display Full Extracted Text
            # --------------------------------------

            with st.expander("View extracted text"):

                st.text_area(
                    "Document content",
                    value=pdf_data["full_text"],
                    height=300,
                    disabled=True
                )

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
            "Unable to process this PDF. "
            "The document may be damaged, "
            "unsupported, or password-protected."
        )

        st.caption(
            f"Error type: {type(error).__name__}"
        )
