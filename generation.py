from embedding import client_gemini


def build_prompt(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    return (
        "Răspunde la întrebare folosind DOAR informațiile din contextul de mai jos. "
        "Dacă răspunsul nu se găsește în context, spune că nu ai suficiente informații.\n\n"
        f"Context:\n{context}\n\n"
        f"Întrebare: {question}"
    )


def generate_answer(question: str, context_chunks: list[str]) -> str:
    prompt = build_prompt(question, context_chunks)
    response = client_gemini.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    return response.text
