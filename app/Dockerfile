FROM python:3.11-slim AS build-env

# Copy files to non-root user home directory
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY src/ requirements.txt ./

# Install dependencies
RUN pip install -U pip && pip install -r requirements.txt

FROM gcr.io/distroless/python3

# Copy files from build stage
COPY --from=build-env /app /app
COPY --from=build-env /usr/local/lib/python3.11/site-packages \
/usr/local/lib/python3.11/site-packages

WORKDIR /app
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

# Start application
CMD ["main.py"]