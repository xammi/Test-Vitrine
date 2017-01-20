FROM python:3.5
MAINTAINER <m.kislenko@corp.mail.ru>

RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends -qq mysql-server mysql-client nginx

WORKDIR /etc/nginx/sites-available
COPY ./deploy/nginx.conf ./vitrine.conf

WORKDIR /etc/nginx/sites-enabled
RUN ln -s ../sites-available/vitrine.conf ./vitrine.conf \
    && rm -f default

WORKDIR /opt/vitrine
COPY ./server ./
COPY ./deploy ./
RUN chmod 777 ./start.sh

RUN pip install -r requirements.txt
EXPOSE 80
CMD ["./start.sh"]