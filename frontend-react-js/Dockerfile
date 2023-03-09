# syntax=docker/dockerfile:1
#FROM node:16.18 as builder
#COPY . /frontend-react-js
#WORKDIR /frontend-react-js
#RUN npm install
#
#FROM node:16.18 as final
#ENV PORT=3000
#ENV NODE_ENV=production
#ENV DISABLE_ESLINT_PLUGIN=true
#RUN apt-get update && apt-get install --no-install-recommends -y curl=7.64.0-4+deb10u5 \
# && apt-get clean \
# && rm -rf /var/lib/apt/lists/*
#WORKDIR /frontend-react-js
#COPY package.json .
#COPY package-lock.json .
#COPY --from=builder ./frontend-react-js/public ./public
#COPY --from=builder ./frontend-react-js/src ./src
#COPY --from=builder ./frontend-react-js/startup.sh ./
## TEMPORARY REMOVED FOR DEV PURPOSES RUN npm i --omit=dev
#RUN npm i
#EXPOSE ${PORT}
#USER node
#ENTRYPOINT [ "./startup.sh" ]

FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]