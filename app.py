import streamlit as st
from rag import RAGChatbot

st.set_page_config(
    page_title="AI PDF Chatbot",
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
# Current PDF
# --------------------------

if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None

# --------------------------
# Sidebar
# --------------------------

with st.sidebar:

    st.header("📄 Upload PDF (Optional)")

    st.write(
        "Upload a PDF to ask questions about it.\n\n"
        "If you don't upload one, the chatbot will answer using its general AI knowledge."
    )

    uploaded_pdf = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_pdf is not None:

        if st.session_state.current_pdf != uploaded_pdf.name:

            with st.spinner("Processing PDF..."):

                bot.load_pdf(uploaded_pdf)

            st.session_state.current_pdf = uploaded_pdf.name

            st.session_state.messages = []

            st.success(f"✅ Loaded: {uploaded_pdf.name}")

# --------------------------
# Status
# --------------------------

if st.session_state.current_pdf:

    st.success(f"📘 Using PDF: {st.session_state.current_pdf}")

else:

    st.info("💡 No PDF uploaded. Chatbot is using Groq's general knowledge.")

# --------------------------
# Display Chat History
# --------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# --------------------------
# Chat Input
# --------------------------

question = st.chat_input("Ask me anything...")

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

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