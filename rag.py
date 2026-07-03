import os
import tempfile

from dotenv import load_dotenv
from groq import Groq

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.embeddings import get_embedding_model

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class RAGChatbot:

    def __init__(self):
        self.embedding_model = get_embedding_model()
        self.vectorstore = None

    def load_pdf(self, uploaded_file):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        loader = PyPDFLoader(temp_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
        )

        chunks = splitter.split_documents(documents)

        self.vectorstore = FAISS.from_documents(
            chunks,
            self.embedding_model,
        )

    def ask(self, question):

        if self.vectorstore is None:
            return "Please upload a PDF first."

        docs = self.vectorstore.similarity_search(
            question,
            k=3,
        )

        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.

If the answer is not found in the context, reply exactly:

"I couldn't find that information in the uploaded PDF."

Context:
{context}

Question:
{question}

Answer:
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        return response.choices[0].message.content