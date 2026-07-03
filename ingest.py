from langchain_community.vectorstores import FAISS

from utils.loader import load_documents
from utils.splitter import split_documents
from utils.embeddings import get_embedding_model

print("Loading documents...")
documents = load_documents()

print("Splitting documents...")
chunks = split_documents(documents)

print("Loading embedding model...")
embedding_model = get_embedding_model()

print("Creating FAISS vector store...")
vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)

print("Saving vector store...")
vectorstore.save_local("vectorstore")

print("\nVector store created successfully!")
print(f"Documents : {len(documents)}")
print(f"Chunks    : {len(chunks)}")