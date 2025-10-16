PYTHON = python3
APP_DIR = app

.PHONY: run-bot-service clean-db


run-bot-service:
	@echo ">>> === Запуск получения сообщений ==="
	$(PYTHON) -m $(APP_DIR).bot_service

clean-db:
	@echo ">>> Удаление локальной базы данных..."
	rm -f my_database.db
	@echo "✅ База данных удалена."
