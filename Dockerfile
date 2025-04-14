# base image
FROM python:3.12-slim-bookworm AS base

WORKDIR /app

# Install Poetry
ENV POETRY_VERSION=2.0.1

# if you located in China, you can use aliyun mirror to speed up
RUN pip install --no-cache-dir poetry==${POETRY_VERSION} uv -i https://mirrors.aliyun.com/pypi/simple/
# Configure Poetry
ENV POETRY_CACHE_DIR=/tmp/poetry_cache
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_CREATE=true
ENV POETRY_REQUESTS_TIMEOUT=60


FROM base AS packages

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config repositories.custom https://mirrors.aliyun.com/pypi/simple/ \
    && poetry install --sync --no-cache --no-root

# production stage
FROM base AS production


EXPOSE 8020

# set timezone
ENV TZ=UTC

WORKDIR /app

# Copy Python environment and packages
ENV VIRTUAL_ENV=/app/.venv
COPY --from=packages ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Copy source code
COPY ./src /app/src
COPY main.py /app/
COPY main_stdio.py /app/

CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8020"]