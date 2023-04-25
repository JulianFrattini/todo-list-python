FROM node:latest

COPY package.json /backend/

WORKDIR /backend/

RUN npm install --save

COPY src /backend/src/

COPY public /backend/public/

EXPOSE 5000

ENV HOST=0.0.0.0

CMD npm run build && npm run production