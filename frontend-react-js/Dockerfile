FROM node:16.18 as builder
COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install

FROM node:16.18 as final
ENV PORT=3000
RUN apt-get update && apt-get install -y curl
WORKDIR /frontend-react-js
COPY --from=builder ./frontend-react-js/public ./public
COPY --from=builder ./frontend-react-js/src ./src
COPY package.json .
COPY package-lock.json .
RUN npm i --omit=dev
EXPOSE ${PORT}
CMD [ "./startup.sh" ]