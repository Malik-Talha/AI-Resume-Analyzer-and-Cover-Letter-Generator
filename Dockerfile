FROM python:3.12-alpine
# installing UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY uv.lock pyproject.toml /app

RUN uv sync --locked

COPY . /app

EXPOSE 8000

CMD ["uv", "run", "main.py"]