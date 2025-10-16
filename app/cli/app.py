import typer
from pyrogram.enums import ChatType

from app.core.db.connection.session import get_sync_session
from app.domains.chats.service import ChatRead, get_chat_service
from app.domains.messages.service import MessageRead, MessageReadFull, get_message_service
from app.domains.users.utils import get_full_name
from app.domains.analyzer.formatter import FormatterService, get_formatter_service
from app.domains.analyzer.analyzer import AnalyzerService, get_analyzer_service

app = typer.Typer()


@app.command()
def main(name: str):
    print(f"Hello {name}")


@app.command("chats")
def get_all_chats():
    with get_sync_session() as session:
        chat_service = get_chat_service(session)
        chats: list[ChatRead] = chat_service.get_all_chats()
        for chat in chats:
            print(
                f"{chat.id}) "
                f"{chat.title if chat.chat_type == ChatType.GROUP else f'{chat.first_name if chat.first_name else ''}{' ' + chat.last_name if chat.last_name else ''}'}"
            )


@app.command("messages")
def get_last_messages(chat_id: int, message_count: int = 20):
    with get_sync_session() as session:
        message_service = get_message_service(session)
        messages: list[MessageReadFull] = message_service.get_last_messages(chat_id, message_count)
        for message in messages:
            full_name = get_full_name(message.user.first_name, message.user.last_name)
            print(
                f"{full_name} ({message.user.username}): {message.text}"
            )


@app.command("msgs")
def get_last_messages1(chat_id: int, message_count: int = 20):
    with get_sync_session() as session:
        formatter_service = get_formatter_service(session)
        messages = formatter_service.create_messages_set(chat_id, message_count)
        print(messages)


@app.command("analyze")
def get_analyzed_messages(chat_id: int, message_count: int = 20):
    with get_sync_session() as session:
        analyzer_service = get_analyzer_service(session)
        response = analyzer_service.analyze_last_messages(chat_id, message_count)
        print(response)


if __name__ == "__main__":
    app()
