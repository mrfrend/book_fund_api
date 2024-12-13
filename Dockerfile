FROM python:latest as builder

RUN pip install poetry
RUN mkdir -p /app
COPY . /app

WORKDIR /app
RUN poetry install

FROM python:latest as base

COPY --from=builder /app /app

WORKDIR /app/src
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 4000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]