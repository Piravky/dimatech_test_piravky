FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY pyproject.toml poetry.lock ./


ENV PATH="/root/.local/bin:$PATH"
RUN poetry install --no-root --no-cache

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY --from=builder /root/.cache/pypoetry /root/.cache/pypoetry
COPY --from=builder /app .
COPY . .

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run python3 src/main.py"]