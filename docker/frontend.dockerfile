FROM node:lts-alpine

WORKDIR /app

COPY ./vue/package*.json ./

RUN npm install

COPY ./vue /app

CMD ["npm", "run", "dev"]
