
import hashlib

import streamlit as st

from agent.smartstudy_agent import run_agent
from services.pdf_service import extract_pdf_text
from services.text_service import create_text_chunks
from services.rag_service import DocumentRetriever
from services.rag_answer_service import answer_from_document
from services.quiz_service import (
    generate_quiz_from_pdf,
    evaluate_quiz_answer,
)
from services.memory_service import (
    record_learning_activity,
    retrieve_learning_history,
)
from services.analytics_service import get_quiz_performance_summary

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SmartStudy",
    page_icon="🎓",
    layout="centered",
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
    format_func=lambda name: name.capitalize(),
)


# --------------------------------------------------
# General AI Assistant
# --------------------------------------------------

st.header("🤖 SmartStudy AI Assistant")

question = st.text_area(
    "What would you like to learn?",
    placeholder="Example: Which topic should I revise first?",
)

if st.button("Ask SmartStudy", type="primary"):

    if not question.strip():

        st.warning("Please enter a question first.")

    else:

        with st.spinner("SmartStudy is thinking..."):

            try:
                answer = run_agent(
                    question=question,
                    provider=provider,
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

            else:

                # Save the completed learning interaction.
                # Memory failures must not discard the AI answer.
                try:
                    record_learning_activity(
                        interaction_type="general_question",
                        topic=question,
                        content=answer,
                    )

                except Exception:
                    st.warning(
                        "Your answer was generated, but "
                        "could not be saved to learning history."
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
    help="Upload a text-based PDF containing lecture notes.",
)


# --------------------------------------------------
# Process Uploaded PDF
# --------------------------------------------------

if uploaded_file is not None:

    try:

        pdf_bytes = uploaded_file.getvalue()

        # Create a unique fingerprint for the PDF.
        file_id = hashlib.sha256(pdf_bytes).hexdigest()

        # Only process when the uploaded PDF changes.
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

            # Save processed PDF data.
            st.session_state["pdf_data"] = pdf_data
            st.session_state["pdf_chunks"] = chunks
            st.session_state["pdf_retriever"] = retriever
            st.session_state["pdf_file_id"] = file_id

            # Clear the previous document's answer.
            st.session_state.pop(
                "document_result", None
            )

            # Clear the previous document's quiz.
            st.session_state.pop(
                "current_quiz", None
            )

            st.session_state.pop(
                "quiz_result", None
            )

            # Clear the previous selected answer.
            st.session_state.pop(
                "quiz_selected_answer", None
            )

        # Load the processed document.
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

                    st.text(
                        chunk["text"]
                    )

                    st.divider()

            # --------------------------------------
            # Preview Full Extracted Text
            # --------------------------------------

            with st.expander("View extracted text"):

                st.text_area(
                    "Document content",
                    value=pdf_data["full_text"],
                    height=300,
                    disabled=True,
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
                key="document_question",
            )

            if st.button(
                "Ask About Document",
                type="primary",
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

                        try:
                            result = answer_from_document(
                                question=document_question,
                                retriever=retriever,
                                provider=provider,
                            )

                        except Exception as error:

                            st.error(
                                "Unable to generate the document answer."
                            )

                            st.caption(
                                f"Error type: {type(error).__name__}"
                            )

                        else:

                            # Save answer between reruns.
                            st.session_state[
                                "document_result"
                            ] = result

                            # Save the learning interaction.
                            try:
                                record_learning_activity(
                                    interaction_type="document_question",
                                    topic=document_question,
                                    content=result["answer"],
                                )

                            except Exception:
                                st.warning(
                                    "The document answer was generated, "
                                    "but could not be saved to learning history."
                                )

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

                            # Find original chunk text.
                            matching_chunk = next(
                                (
                                    chunk
                                    for chunk in chunks
                                    if chunk["chunk_id"]
                                    == source["chunk_id"]
                                ),
                                None,
                            )

                            if matching_chunk:

                                st.text(
                                    matching_chunk["text"]
                                )

                            st.divider()

            # --------------------------------------
            # AI Quiz Generation
            # --------------------------------------

            st.divider()

            st.subheader("📝 AI Quiz Generator")

            st.write(
                "Generate a multiple-choice question "
                "from your uploaded lecture notes."
            )

            quiz_topic = st.text_input(
                "Enter a topic from your lecture notes:",
                placeholder="Example: primary key",
                key="quiz_topic",
            )

            if st.button("Generate Quiz"):

                if not quiz_topic.strip():

                    st.warning(
                        "Please enter a quiz topic."
                    )

                else:

                    with st.spinner(
                        "Generating a quiz from "
                        "your lecture notes..."
                    ):

                        try:

                            quiz = generate_quiz_from_pdf(
                                chunks=chunks,
                                topic=quiz_topic,
                                provider=provider,
                            )

                            # Save the new quiz.
                            st.session_state[
                                "current_quiz"
                            ] = quiz

                            # Remove the previous score.
                            st.session_state.pop(
                                "quiz_result", None
                            )

                            # Reset the previous answer.
                            st.session_state.pop(
                                "quiz_selected_answer", None
                            )

                        except ValueError as error:

                            st.warning(
                                str(error)
                            )

                        except Exception as error:

                            st.error(
                                "Unable to generate the quiz."
                            )

                            st.caption(
                                f"Error type: {type(error).__name__}"
                            )

            # --------------------------------------
            # Display Generated Quiz
            # --------------------------------------

            if "current_quiz" in st.session_state:

                quiz = st.session_state[
                    "current_quiz"
                ]

                st.markdown("### Quiz Question")

                st.write(
                    quiz["question"]
                )

                # ----------------------------------
                # Student Answer Selection
                # ----------------------------------

                selected_answer = st.radio(
                    "Choose your answer:",
                    options=range(4),
                    format_func=lambda index: (
                        f"{chr(65 + index)}. "
                        f"{quiz['options'][index]}"
                    ),
                    index=None,
                    key="quiz_selected_answer",
                    disabled=(
                        "quiz_result" in st.session_state
                    ),
                )

                # ----------------------------------
                # Submit Answer
                # ----------------------------------

                if st.button(
                    "Submit Answer",
                    disabled=(
                        "quiz_result" in st.session_state
                    ),
                ):

                    if selected_answer is None:

                        st.warning(
                            "Please select an answer first."
                        )

                    else:

                        try:

                            # Score the answer using Python.
                            result = evaluate_quiz_answer(
                                quiz=quiz,
                                selected_answer=selected_answer,
                            )

                            # Store the result between reruns.
                            st.session_state[
                                "quiz_result"
                            ] = result

                        except Exception as error:

                            st.error(
                                "Unable to evaluate the quiz answer."
                            )

                            st.caption(
                                f"Error type: {type(error).__name__}"
                            )

                        else:

                            # Save the completed quiz result.
                            try:
                                record_learning_activity(
                                    interaction_type="quiz",
                                    topic=quiz["question"],
                                    content=(
                                        f"Selected answer: "
                                        f"{quiz['options'][selected_answer]}\n"
                                        f"Correct answer: "
                                        f"{quiz['options'][result['correct_answer']]}\n"
                                        f"Explanation: {result['explanation']}"
                                    ),
                                    score=result["score"],
                                )

                            except Exception:
                                st.warning(
                                    "Your quiz was evaluated, but "
                                    "the result could not be saved."
                                )

                # ----------------------------------
                # Display Quiz Result
                # ----------------------------------

                if "quiz_result" in st.session_state:

                    result = st.session_state[
                        "quiz_result"
                    ]

                    if result["is_correct"]:

                        st.success(
                            "Correct answer!"
                        )

                    else:

                        st.error(
                            "Incorrect answer."
                        )

                    # Display score.
                    st.write(
                        f"**Score:** {result['score']} / 1"
                    )

                    # Display correct answer.
                    correct_index = result[
                        "correct_answer"
                    ]

                    st.write(
                        "**Correct Answer:** "
                        f"{chr(65 + correct_index)}. "
                        f"{quiz['options'][correct_index]}"
                    )

                    # Display explanation.
                    st.write(
                        "**Explanation:** "
                        f"{result['explanation']}"
                    )

        else:

            st.warning(
                "No readable text was found in this PDF. "
                "It may contain scanned images instead "
                "of selectable text."
            )

    except ValueError as error:

        st.warning(
            str(error)
        )

    except Exception as error:

        st.error(
            "Unable to process the document "
            "or generate an answer."
        )

        st.caption(
            f"Error type: {type(error).__name__}"
        )

else:

    # Clear stored document data if upload is removed.
    for key in [
        "pdf_file_id",
        "pdf_data",
        "pdf_chunks",
        "pdf_retriever",
        "document_result",
        "current_quiz",
        "quiz_result",
        "quiz_selected_answer",
    ]:

        st.session_state.pop(
            key, None
        )


# --------------------------------------------------
# Persistent Learning History
# --------------------------------------------------

st.divider()

st.header("📚 Learning History")

st.write(
    "View your recently saved questions, "
    "document answers, and quiz results."
)

if st.button("Refresh Learning History"):

    try:

        history = retrieve_learning_history(
            limit=10
        )

        st.session_state[
            "learning_history"
        ] = history

    except Exception as error:

        st.error(
            "Unable to retrieve learning history."
        )

        st.caption(
            f"Error type: {type(error).__name__}"
        )


if "learning_history" in st.session_state:

    history = st.session_state[
        "learning_history"
    ]

    if not history:

        st.info(
            "No learning activity has been saved yet."
        )

    else:

        for record in history:

            with st.expander(
                f"{record['interaction_type']} — "
                f"{record['topic'][:60]}"
            ):

                st.write(
                    f"**Date:** {record['created_at']}"
                )

                st.write(
                    f"**Topic:** {record['topic']}"
                )

                st.write("**Content:**")

                st.text(
                    record["content"]
                )

                if record["score"] is not None:

                    st.write(
                        f"**Score:** {record['score']} / 1"
                    )


# ---------------------------------------------------------
# Learning Analytics Dashboard
# ---------------------------------------------------------

st.divider()

st.header("📊 Learning Analytics")

st.write(
    "Track your quiz performance and monitor "
    "your learning progress."
)

try:
    statistics = get_quiz_performance_summary()

    total_quizzes = statistics["total_quizzes"]
    correct_answers = statistics["correct_answers"]
    incorrect_answers = statistics["incorrect_answers"]
    accuracy = statistics["accuracy"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Total Quizzes",
            value=total_quizzes,
        )

        st.metric(
            label="Correct Answers",
            value=correct_answers,
        )

    with col2:
        st.metric(
            label="Accuracy",
            value=f"{accuracy:.2f}%",
        )

        st.metric(
            label="Incorrect Answers",
            value=incorrect_answers,
        )

    st.subheader("Quiz Accuracy")

    if total_quizzes > 0:
        st.progress(accuracy / 100)

        st.caption(
            f"You answered {correct_answers} "
            f"out of {total_quizzes} quizzes correctly."
        )

    else:
        st.info(
            "No completed quizzes yet. "
            "Generate and answer a quiz to "
            "start tracking your progress."
        )

except Exception as error:
    st.error(
        "Unable to load learning analytics: "
        f"{error}"
    )
