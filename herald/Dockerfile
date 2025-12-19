ARG PYTHON_VERSION=3.14
ARG OS_VERSION=slim-trixie

FROM python:$PYTHON_VERSION-$OS_VERSION

RUN groupadd -g 1000 robot \
    && useradd -u 1000 -g 1000 \
    -M robot

RUN python -m venv venv

ENV PATH="/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --chown=1000:1000 app /app
COPY --chown=1000:1000 requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

USER 1000

CMD ["python", "app.py"]