# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster as builder
WORKDIR /backend-flask
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_ENV=development

FROM python:3.10-slim-buster as final
ENV PORT=4567
# ENV FLASK_ENV=production Temporary removed for development comfort
ENV FLASK_ENV=development
ENV OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
ENV OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
ENV OTEL_SERVICE_NAME: "${HONEYCOMB_SERVICE_NAME}"
RUN apt-get update && apt-get install --no-install-recommends -y curl=7.64.0-4+deb10u5 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /backend-flask
COPY --from=builder ./backend-flask .
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE ${PORT}
USER daemon
ENTRYPOINT [ "./startup.sh" ]