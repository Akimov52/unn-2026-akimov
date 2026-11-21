# Telegram echo bot

Учебный Telegram-бот: повторяет **точно тот же текст**, который получил. Фото, стикеры,
голосовые сообщения, callback-запросы и любые другие нетекстовые обновления игнорируются.

## Архитектура

- `bot/messenger.py` — интерфейс `Messenger`, от которого зависят остальные компоненты.
- `bot/telegram_messenger.py` — HTTP-адаптер Telegram Bot API. Все запросы идут через адрес,
  собранный из `TELEGRAM_BASE_URL` и `TELEGRAM_TOKEN`.
- `bot/long_polling.py` — получение обновлений пачками и управление `offset`.
- `bot/dispatcher.py` — передача обновлений зарегистрированным обработчикам.
- `bot/handlers/message_text.py` — единственный handler; обрабатывает только текстовые сообщения.
- `tests/` — отдельные тесты long polling, dispatcher и handler.

Поток зависимостей: `main → long polling → Dispatcher → Handler → Messenger`. Конкретный
`TelegramMessenger` создаётся только в точке входа и передаётся компонентам через интерфейс
`Messenger` (Dependency Inversion Principle).

## Переменные окружения

| Переменная | Обязательная | Описание |
|---|---:|---|
| `TELEGRAM_TOKEN` | Да | Токен бота от BotFather |
| `TELEGRAM_BASE_URL` | Да | Базовый URL Bot API, например `https://api.telegram.org` |

## Локальный запуск

```bash
uv sync --group dev

# Linux/macOS
TELEGRAM_TOKEN="<token>" TELEGRAM_BASE_URL="https://api.telegram.org" uv run python -m bot
```

## Проверки

```bash
make install
make test
make ruff-cs-check       # проверить форматирование
make ruff-cs-fix         # исправить форматирование
make ruff-linter-check   # проверить линтер
make ruff-linter-fix     # автоматически исправить замечания линтера
make mypy-check          # проверить типы
make check               # выполнить все проверки
```

## Docker

```bash
docker build -t telegram-echo-bot:local .

docker run --rm \
  -e TELEGRAM_TOKEN="<token>" \
  -e TELEGRAM_BASE_URL="https://api.telegram.org" \
  telegram-echo-bot:local
```

## GitHub Actions и GHCR

Workflow `.github/workflows/ci.yml` запускает проверки и сборку Docker-образа при pull request
в `master`. После push/merge в `master` он также публикует образы с тегами `latest` и commit SHA
в `ghcr.io/<owner>/<repository>`. # Комментарий для PR
