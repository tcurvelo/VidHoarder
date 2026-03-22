FROM python:3.12-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install  \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


RUN --mount=type=cache,target=/root/.cache/uv \
--mount=type=bind,source=uv.lock,target=uv.lock \
--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
uv sync --frozen --no-install-project

FROM python:3.12-slim AS prod

WORKDIR /app
EXPOSE 3000
ENV PATH=/app/.venv/bin:$PATH

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
COPY --from=base /app/.venv /app/.venv
COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

CMD ["./main.py"]
