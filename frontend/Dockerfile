FROM node:latest

COPY package.json /frontend/

WORKDIR /frontend/

RUN npm install

COPY src /frontend/src/

COPY public /frontend/public/

EXPOSE 5000

ENV HOST=0.0.0.0

CMD npm run build && npm run production