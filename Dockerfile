# ---------------- Base -----------------------
FROM python:3.12-alpine AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    UV_PYTHON_DOWNLOADS=0 \
    APP_PATH="/app"

ENV VIRTUAL_ENV="$APP_PATH/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR $APP_PATH
# ----------------------------------------------

# --------------- Base Builder -----------------
FROM python-base AS base-builder

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    git \
    libffi-dev \
    openssl-dev

COPY --from=ghcr.io/astral-sh/uv:0.8.0 /uv /uvx /bin/

COPY ./pyproject.toml ./uv.lock ./
COPY ./src ./src
# ----------------------------------------------

# ----------------- Base Runtime ---------------
FROM python-base AS base-runtime

RUN apk add --no-cache \
    curl \
    libstdc++

RUN adduser -D -h /home/appuser -s /bin/sh appuser

USER appuser
# ----------------------------------------------

# =================== Web ======================
FROM base-builder AS web-builder
RUN uv sync --no-dev --group web --no-editable --frozen

FROM base-runtime AS web-runtime
COPY --from=web-builder $VIRTUAL_ENV $VIRTUAL_ENV
# ==============================================

# =================== Worker ===================
FROM base-builder AS worker-builder
RUN uv sync --no-dev --group worker --no-editable --frozen

FROM base-runtime AS worker-runtime
COPY --from=worker-builder $VIRTUAL_ENV $VIRTUAL_ENV
# ==============================================
