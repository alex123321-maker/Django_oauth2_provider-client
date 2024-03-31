FROM python:3.11-slim

WORKDIR /client

ENV PYTHONDONTWRITEBYTECODE 1


COPY . /client/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]