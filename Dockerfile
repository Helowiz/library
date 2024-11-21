FROM python:3.12

WORKDIR /home/library

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -q -y update \
    && apt-get install -y netcat-openbsd \
    && apt-get clean

RUN pip install --upgrade pip
COPY requirements.txt /home/library/requirements.txt
RUN pip install -r requirements.txt

COPY . /home/library/
RUN chmod +x /home/library/entrypoint.sh

ENTRYPOINT ["/home/library/entrypoint.sh"]    