#!/bin/bash

mkdir /var/lib/mysql
mkfifo /var/run/mysqld/mysqld.sock
chown mysql:mysql -R /var/lib/mysql
chmod 0777 /var/run/mysqld/mysqld.sock
mysql_install_db

service mysql start

mysql -e "create database vitrine_db charset utf8"
mysql -e "grant all privileges on vitrine_db.* to vitrine_user identified by '11'"
mysql vitrine_db < start_dump.sql

python manage.py runserver 0.0.0.0:8000