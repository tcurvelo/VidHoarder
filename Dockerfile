FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install  \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 3000

RUN --mount=type=cache,target=/root/.cache/uv \
--mount=type=bind,source=uv.lock,target=uv.lock \
--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
uv sync --frozen --no-install-project

ENV PATH=/app/.venv/bin:$PATH

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

CMD ["./main.py"]
