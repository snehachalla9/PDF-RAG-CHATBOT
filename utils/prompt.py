def build_prompt(
    query,
    context,
    history,
    sources=None
):
    sources_text = ""
    if sources:
        sources_text = f"\nSources:\n{sources}"

    prompt = f"""
You are a helpful AI assistant.

Use the provided context to answer the question.

If the answer can be inferred from the context,
provide the answer.

If the answer is not available in the context,
say "I couldn't find that information in the document."

Chat History:
{history}

Context:
{context}

{sources_text}

Question:
{query}

Answer:
"""

    return prompt