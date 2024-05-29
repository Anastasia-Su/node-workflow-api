FROM python:3.11.7-slim
LABEL maintainer="anastasia.su.po@gmail.com"
ENV PYTHONUNBUFFERED 1

WORKDIR app/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update  \
    && apt-get install -y --no-install-recommends ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p /vol/web/media
RUN chmod -R 755 /vol/web/

CMD ["./start.sh"]
