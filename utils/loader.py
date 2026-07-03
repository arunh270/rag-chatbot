import os
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)


def load_documents(folder_path="docs"):
    """
    Load all .txt and .pdf documents from a folder.
    """

    documents = []

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())

        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())

    return documents