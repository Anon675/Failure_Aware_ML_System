class PromptBuilder:
    """
    Builds RAG-aware prompts.
    """

    def build(self, user_input, retrieved_docs):
        context_block = "\n\n".join(retrieved_docs)

        return f"""
You are a precise AI assistant.
Use ONLY the provided context to answer.

Context:
{context_block}

Question:
{user_input}

Answer:
"""
