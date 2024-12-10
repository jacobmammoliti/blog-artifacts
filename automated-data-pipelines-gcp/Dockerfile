ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim

RUN apt-get update && pip install --upgrade pip \
    && pip install --disable-pip-version-check --no-cache-dir gspread scrapy

COPY . /app

WORKDIR /app/bookstoscrape

USER nobody

ENTRYPOINT ["scrapy", "crawl", "books_spider"]