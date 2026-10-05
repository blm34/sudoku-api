FROM python:3.14-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.10.0 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install third party dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy sudoku-api source
COPY sudoku ./sudoku/
COPY README.md LICENSE ./

# Build sudoku-api wheel
ARG APP_VERSION=0.0.0
ENV SETUPTOOLS_SCM_PRETEND_VERSION_FOR_SUDOKU_API="${APP_VERSION}"
RUN uv build --wheel --out-dir /tmp/dist

# Install the wheel into the venv
RUN uv pip install /tmp/dist/*.whl


FROM python:3.14-slim AS runtime

WORKDIR /app

COPY --from=builder /app/.venv/ ./.venv/

RUN useradd --create-home --uid 1000 appuser
USER appuser

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "sudoku.main:app", "--host", "0.0.0.0", "--port", "8000"]
