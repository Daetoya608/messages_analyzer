from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from sqlalchemy.orm import Session

from app.domains.analyzer.llm import LLMService, get_llm_service
from app.domains.analyzer.formatter import FormatterService, get_formatter_service
from app.domains.analyzer.analyzer.utils import SYSTEM_PROMPT


class AnalyzerService:
    def __init__(self, llm_service: LLMService, formatter_service: FormatterService):
        self.llm_service = llm_service
        self.formatter_service = formatter_service

    def analyze_last_messages(self, chat_id: int, message_count: int) -> str:
        chat_log = self.formatter_service.create_messages_set(chat_id, message_count)
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Проанализируй лог и дай только важное:\n{chat_log}")
        ]
        response = self.llm_service.ask_llm(messages)
        return response


def get_analyzer_service(session: Session, chat_ollama: ChatOllama = None):
    formatter_service = get_formatter_service(session)
    llm_service = get_llm_service(chat_ollama)
    return AnalyzerService(llm_service, formatter_service)
