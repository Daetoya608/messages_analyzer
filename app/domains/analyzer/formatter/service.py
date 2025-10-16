from functools import reduce

from sqlalchemy.orm import Session

from app.domains.messages import MessageService, get_message_service


class FormatterService:
    def __init__(self, message_service: MessageService):
        self.message_service = message_service

    def create_messages_set(self, chat_id: int, message_count: int):
        messages = self.message_service.get_last_messages(chat_id, message_count)
        return "\n".join(map(str, messages))


def get_formatter_service(session: Session) -> FormatterService:
    message_service = get_message_service(session)
    return FormatterService(message_service)
