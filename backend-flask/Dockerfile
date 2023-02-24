FROM python:3.10-slim-buster as builder
WORKDIR /backend-flask
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_ENV=development

FROM python:3.10-slim-buster as final
ENV PORT=4567
RUN apt-get update && apt-get install -y curl
WORKDIR /backend-flask
COPY --from=builder ./backend-flask .
RUN pip3 install -r requirements.txt
ENV FLASK_ENV=production
EXPOSE ${PORT}
CMD [ "./startup.sh" ]