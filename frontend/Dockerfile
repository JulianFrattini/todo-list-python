FROM node:latest

# Install operating system dependencies required by Cypress Test Runner
RUN apt-get update && apt-get install -y \
    libgtk2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    libnotify-dev \
    libnss3 \
    libxss1 \
    libasound2 \
    libxtst6 \
    xauth \
    xvfb

COPY package.json /frontend/

WORKDIR /frontend/

RUN npm install

COPY src /frontend/src/

COPY public /frontend/public/

# EXPOSE 3000 # Uncomment if you are not using compose and update the port if needed

ENV HOST=0.0.0.0

CMD npm run build && npm run production