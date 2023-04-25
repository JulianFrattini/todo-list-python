# this Dockerfile won't work on it's own, as it requires there to be a
# mongodb database running, and a corresponding configuration.
# use the docker compose file in the root directory instead.
# if for some reason you want to use this Dockerfile/image on its own,
# uncomment the MONGO_URL line below and insert the relevant information
# (remember that you'll also need to make the mongodb database you use
# available to the Docker containers, possibly by port bindings). 
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.pip requirements.pip

RUN pip3 install -r requirements.pip

COPY . .

# ENV FLASK_BIND_IP=0.0.0.0
# ENV MONGO_URL=mongodb://dockerUser:dockerPass@mongodb:27017/edutaskDb

CMD [ "python", "./main.py"]
