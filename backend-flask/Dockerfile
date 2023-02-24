# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster as builder
WORKDIR /backend-flask
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_ENV=development

FROM python:3.10-slim-buster as final
ENV PORT=4567
ENV FLASK_ENV=production
RUN apt-get update && apt-get install -y curl
WORKDIR /backend-flask
COPY --from=builder ./backend-flask .
RUN pip3 install -r requirements.txt
EXPOSE ${PORT}
USER daemon
ENTRYPOINT [ "./startup.sh" ]