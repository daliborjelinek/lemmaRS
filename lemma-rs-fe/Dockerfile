# build stage
FROM node:16-alpine as build-stage
WORKDIR /app
ARG VUE_APP_API_URL
ENV VUE_APP_API_URL=$VUE_APP_API_URL
COPY package*.json ./
RUN npm install
COPY ./ .
RUN npm run build

FROM nginx:latest as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf