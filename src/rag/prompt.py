def build_prompt(context, question):
    return f"""
You are an assistant answering questions strictly using the provided context.
If the answer is not found in the context, say:
"Bu bilgi verilen PDF'te yer almıyor."

Context:
{context}

Question:
{question}

Answer:
"""