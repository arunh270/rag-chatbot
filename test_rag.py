from rag import RAGChatbot

bot = RAGChatbot()

question = input("Ask a question: ")

results = bot.retrieve(question)

print("\nTop Retrieved Chunks\n")

for i, doc in enumerate(results, start=1):

    print("=" * 60)
    print(f"Chunk {i}")
    print("=" * 60)

    print(doc.page_content)
    print()