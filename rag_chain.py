import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    # model="gemini-1.5-flash"
    model="gemini-2.5-flash"
)

def get_answer(query, docs):

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
    Answer only from the context.

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)

    return response.content