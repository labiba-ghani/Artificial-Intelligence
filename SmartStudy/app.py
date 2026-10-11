
import streamlit as st

from agent.smartstudy_agent import run_agent


# Configure the browser page
st.set_page_config(
    page_title="SmartStudy",
    page_icon="🎓",
    layout="centered"
)


# Application heading
st.title("🎓 SmartStudy")

st.write(
    "Your AI-powered personalized learning assistant."
)


# Choose which AI provider to use
provider = st.selectbox(
    "Choose your AI provider:",
    ["groq", "ollama"],
    format_func=lambda name: name.capitalize()
)


# Student enters a question
question = st.text_area(
    "What would you like to learn?",
    placeholder="Example: Which topic should I revise first?"
)


# Run the agent when the button is clicked
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
