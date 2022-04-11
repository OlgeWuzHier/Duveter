FROM node:16.13.2-alpine as build

WORKDIR /front

COPY package.json package.json

RUN npm install

COPY . .

ENV NODE_ENV=production

RUN npm run build -- --configuration production

FROM nginx:1.21.5-alpine

COPY --from=build /front/dist/ /usr/share/nginx/html

EXPOSE 80
