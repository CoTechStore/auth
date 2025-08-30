# ---------------- Base -----------------------
FROM python:3.12-slim-bookworm AS python-base

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

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.8.0 /uv /uvx /bin/

COPY ./pyproject.toml ./uv.lock ./

COPY ./src ./src
# ----------------------------------------------

# --------------- Base Production --------------
FROM python-base AS base-production

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --no-log-init --shell /bin/bash appuser

USER appuser
# ----------------------------------------------

# =================== Web ======================
FROM base-builder AS web-builder
RUN uv sync --no-dev --group web --no-editable --frozen

FROM base-production AS web-production
COPY --from=web-builder $VIRTUAL_ENV $VIRTUAL_ENV
# ==============================================

# =================== Worker ===================
FROM base-builder AS worker-builder
RUN uv sync --no-dev --group worker --no-editable --frozen

FROM base-production AS worker-production
COPY --from=worker-builder $VIRTUAL_ENV $VIRTUAL_ENV
# ==============================================
