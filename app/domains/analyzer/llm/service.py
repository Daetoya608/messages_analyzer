from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from app.domains.analyzer.llm.utils import get_ollama_llm, strip_think


class LLMService:
    def __init__(self, chat_ollama: ChatOllama = None):
        self.llm = chat_ollama if chat_ollama else get_ollama_llm()
        self.chain = self.llm | StrOutputParser

    def ask_llm(self, request_for_model: str | list) -> str:
        response_llm = self.llm.invoke(request_for_model)
        only_text = strip_think(response_llm.content if hasattr(response_llm, "content") else str(response_llm))
        return only_text


def get_llm_service(chat_ollama: ChatOllama = None):
    return LLMService(chat_ollama)
