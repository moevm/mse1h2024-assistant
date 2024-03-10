FROM node:20.11.1-alpine as build-stage

WORKDIR /frontend

COPY . /frontend

RUN npm install

RUN chmod -R a+x node_modules

RUN npm run build

FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /frontend/dist /usr/share/nginx/html

COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;"]