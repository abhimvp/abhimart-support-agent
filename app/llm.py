from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings


def get_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        api_key=settings.gemini_api_key,
        timeout=30,
        max_retries=2,
    )