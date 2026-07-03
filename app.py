import streamlit as st
from rag import RAGChatbot

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI PDF Chatbot")

# --------------------------
# Create chatbot once
# --------------------------

if "bot" not in st.session_state:
    st.session_state.bot = RAGChatbot()

bot = st.session_state.bot

# --------------------------
# Chat History
# --------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------
# Track Current PDF
# --------------------------

if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None

# --------------------------
# Sidebar
# --------------------------

with st.sidebar:
    st.header("📄 Upload PDF")

    uploaded_pdf = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_pdf is not None:

        # Process only if it's a NEW PDF
        if st.session_state.current_pdf != uploaded_pdf.name:

            with st.spinner("Processing PDF..."):

                bot.load_pdf(uploaded_pdf)

            st.session_state.current_pdf = uploaded_pdf.name

            # Clear old chat
            st.session_state.messages = []

            st.success(f"✅ {uploaded_pdf.name} loaded successfully!")

# --------------------------
# Show Current PDF
# --------------------------

if st.session_state.current_pdf:

    st.info(f"📘 Current PDF: {st.session_state.current_pdf}")

else:

    st.warning("Please upload a PDF from the sidebar.")

# --------------------------
# Display Chat History
# --------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# --------------------------
# Chat Input
# --------------------------

question = st.chat_input("Ask anything about the uploaded PDF...")

if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = bot.ask(question)

            st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )