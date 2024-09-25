FROM python:3.11-slim AS builder

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM gcr.io/distroless/python3-debian12:latest

COPY --from=builder /usr/local/lib/python3.11/site-packages /app/site-packages

WORKDIR /app/src

COPY src/main.py .

ENV PYTHONPATH=/app/site-packages

CMD ["main.py"]