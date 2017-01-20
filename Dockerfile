FROM python:3.5
MAINTAINER <m.kislenko@corp.mail.ru>

RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends -qq mysql-server mysql-client nginx \
    && rm -rf /var/lib/mysql

WORKDIR /opt/vitrine
COPY ./server ./
COPY ./deploy ./
RUN chmod 777 ./start.sh

RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["./start.sh"]