
# baze immage
from python:alpine3.10


# env variable
ENV APP /web_HW5

# working directory
WORKDIR $APP

# volume
# VOLUME /storage

# copy my project
COPY . .


RUN pip install --upgrade pip
RUN apk update
RUN apk add build-base python3-dev


# run requirements
RUN pip install -r requirements.txt

RUN pip install aiohttp

# port set
EXPOSE 8080


ENTRYPOINT ["python", "server.py" ]