FROM python:3
ADD . /app/
WORKDIR /app
RUN set -xe \
    && apt-get update -q -y \
    && apt-get install python3-pip postgresql-client -q -y
RUN pip install -r reqs/app_requirements.txt
EXPOSE 8000