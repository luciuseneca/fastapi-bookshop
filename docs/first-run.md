# Первый запуск на новом компьютере

Эта инструкция описывает полный запуск проекта на чистом компьютере. Основное
приложение и инфраструктура работают в Docker, но Ollama сейчас запускается на
хосте отдельно и не входит в `docker-compose.yml`.

## Что установить

| Инструмент | Обязательно | Для чего |
|---|---:|---|
| Git | Да, если проект клонируется из Git | Получение исходного кода |
| Docker Desktop | Да для macOS/Windows | Docker Engine, CLI, BuildKit и Compose v2 |
| Docker Engine + Compose plugin | Альтернатива для Linux | Запуск контейнеров |
| Ollama | Да для полной функциональности | Локальные эмбеддинги и малые LLM |
| OpenSSL | Да | Создание локальной пары JWT-ключей |
| OpenAI API key | По выбору | Основная LLM `gpt-4.1` в конфигурации по умолчанию |

Официальные страницы установки:

- [Docker](https://docs.docker.com/get-started/get-docker/);
- [Docker Compose](https://docs.docker.com/compose/install/);
- [Ollama](https://ollama.com/download).

На хосте **не нужно** устанавливать Python, Poetry, PostgreSQL, Redis,
RabbitMQ, Elasticsearch или Qdrant. Они устанавливаются в образ приложения
или запускаются отдельными Compose-сервисами.

Перед продолжением проверьте:

```bash
git --version
docker version
docker compose version
ollama --version
openssl version
```

Docker daemon и Ollama должны быть запущены. При первой сборке также нужен
доступ к Docker Hub, PyPI, GitHub и репозиторию образов Elastic.

## Какие модели нужны

Проект обращается к следующим локальным моделям Ollama:

| Модель | Где используется | Настройка |
|---|---|---|
| `bge-m3` | Эмбеддинги книг, FAQ и профилей рекомендаций | Задана в коде, размер вектора `1024` |
| `llama3.1:8b` | Роутер агента, короткие ответы и support-бот | Задана в `.env.example` и частично в коде |

Установите их до запуска приложения:

```bash
ollama pull bge-m3
ollama pull llama3.1:8b
ollama list
```

Проверьте API Ollama:

```bash
curl http://127.0.0.1:11434/api/tags
```

На Linux Ollama часто слушает только loopback-интерфейс. Чтобы контейнеры
могли обратиться к ней через `host.docker.internal`, настройте сервис Ollama
на прослушивание `0.0.0.0:11434`, например через systemd override:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Затем перезапустите Ollama. Не публикуйте порт `11434` в недоверенную сеть;
при необходимости ограничьте доступ firewall.

## Подготовка проекта

### 1. Создать `.env`

macOS/Linux/Git Bash:

```bash
cp .env.example .env
```

PowerShell:

```powershell
Copy-Item .env.example .env
```

Минимально замените в `.env`:

- `FASTAPI__APP__SECRET_KEY` — случайная строка, например результат
  `openssl rand -base64 32`;
- `FASTAPI__LLM__API_KEY` — настоящий OpenAI API key, если основная модель
  остаётся `gpt-4.1`;
- Stripe, SMTP и Google OAuth — только если эти функции будут использоваться.

Какие внешние доступы нужны отдельным функциям:

| Функция | Что заполнить |
|---|---|
| Обычный каталог и локальные рекомендации | Внешние аккаунты не нужны |
| Основной AI-агент с `gpt-4.1` | `FASTAPI__LLM__API_KEY` |
| Регистрация с отправкой OTP | `FASTAPI__SMTP__DSN`, адреса отправителя |
| Вход через Google | `FASTAPI__OAUTH_GOOGLE__CLIENT_ID` и `CLIENT_SECRET` |
| Оплата | Stripe secret key и webhook secret |

Шаблонные значения позволяют разобрать конфигурацию, но соответствующая
интеграция завершится ошибкой при первом реальном обращении к ней.

Значения URL с именами `postgres`, `redis`, `rabbitmq`, `qdrant` и
`elasticsearch` менять не нужно: это DNS-имена сервисов внутри Compose-сети.
Для Ollama должны остаться адреса хоста:

```dotenv
FASTAPI__OLLAMA__URL=http://host.docker.internal:11434
FASTAPI__LLM__ROUTER_BASE_URL=http://host.docker.internal:11434/v1
```

Если OpenAI использовать не нужно, основную LLM тоже можно направить в Ollama:

```dotenv
FASTAPI__LLM__BASE_URL=http://host.docker.internal:11434/v1
FASTAPI__LLM__API_KEY=ollama
FASTAPI__LLM__CHAT_MODEL=llama3.1:8b
```

### 2. Создать JWT-ключи

```bash
mkdir -p cert
openssl genpkey -algorithm RSA \
  -out cert/jwt-private.pem \
  -pkeyopt rsa_keygen_bits:2048
openssl pkey \
  -in cert/jwt-private.pem \
  -pubout \
  -out cert/jwt-public.pem
```

В PowerShell сначала выполните `New-Item -ItemType Directory -Force cert`, а
команды OpenSSL запустите без символов переноса `\` — каждую одной строкой.
Каталог `cert` и `.env` исключены из Git; приватный ключ нельзя коммитить.

## Первый запуск

Порядок важен: сначала инфраструктура, затем схема хранилищ, затем все процессы
приложения.

### 1. Собрать образ приложения

```bash
docker compose build
```

### 2. Запустить хранилища и очередь

```bash
docker compose up -d postgres redis rabbitmq elasticsearch qdrant
docker compose ps
```

Дождитесь состояния `healthy` у PostgreSQL, RabbitMQ и Elasticsearch.

### 3. Создать схему PostgreSQL, коллекции Qdrant и индексы Elasticsearch

```bash
docker compose run --rm fastapi python -m app.cli init-db
```

Команда идемпотентна: её можно запускать повторно. Она создаёт схему, но не
добавляет демонстрационные книги. Если у вас есть отдельный SQL-дамп с данными,
восстанавливайте его только в пустую БД согласно инструкции к этому дампу, а
после восстановления выполните миграции.

### 4. Запустить весь проект

```bash
docker compose up -d
docker compose ps
docker compose logs --tail=100 fastapi taskiq_worker llm_consumer
```

При старте FastAPI ставит в очередь первичную индексацию книг и FAQ. Поэтому
Ollama и обе модели должны быть готовы до этого шага.

## Проверка результата

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/ready
```

Ожидается:

```json
{"status":"ok"}
```

`/ready` дополнительно должен показать `ok` для PostgreSQL и Redis. Интерфейс
приложения доступен по адресу <http://127.0.0.1:8000>.

Проверка инфраструктуры:

```bash
curl http://127.0.0.1:9200/_cluster/health
curl http://127.0.0.1:6333/collections
```

RabbitMQ Management UI: <http://127.0.0.1:15672> (для dev-конфигурации по
умолчанию логин и пароль — `guest`).

## Типичные ошибки

| Ошибка | Причина | Что сделать |
|---|---|---|
| `Connection refused` к `host.docker.internal:11434` | Ollama не запущена или недоступна из контейнера | Запустить Ollama; на Linux проверить `OLLAMA_HOST` и firewall |
| `model ... not found` | Модель не загружена | Выполнить `ollama pull bge-m3` и `ollama pull llama3.1:8b` |
| `No such file ... jwt-private.pem` | Нет JWT-ключей или неверный путь | Создать оба файла в `./cert`; внутри контейнера пути должны начинаться с `/cert/` |
| Ошибка Pydantic при импорте приложения | В `.env` отсутствует обязательная секция | Пересоздать файл из актуального `.env.example` и перенести секреты |
| `relation ... does not exist` | Не применены миграции | Выполнить `docker compose run --rm fastapi python -m app.cli init-db` |
| Ошибка OpenAI `401` | Оставлен шаблонный API key | Указать настоящий ключ или направить основную LLM в локальную Ollama |
| Elasticsearch завершается с нехваткой памяти | Docker VM получила мало памяти | Увеличить доступную Docker память; в Compose heap Elasticsearch равен 512 МБ |
| RabbitMQ сообщает о нехватке места | Свободного места меньше установленного лимита | Освободить место; dev-конфигурация требует запас не менее 2 ГБ для RabbitMQ |

Для диагностики сначала используйте:

```bash
docker compose ps
docker compose logs --tail=200 <service>
docker compose config
ollama list
```

Не используйте `docker compose down -v` для исправления проблем запуска: эта
команда удаляет тома и данные PostgreSQL, Redis, RabbitMQ, Elasticsearch и
Qdrant.

## Повторный запуск

```bash
docker compose up -d
```

После изменения `pyproject.toml`, `poetry.lock` или `Dockerfile`:

```bash
docker compose up -d --build
```

Остановить процессы без удаления контейнеров и данных:

```bash
docker compose stop
```
