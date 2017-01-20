#!/bin/bash

chown mysql:mysql -R /var/lib/mysql
mysql_install_db

service mysql start
service nginx start

echo "create database vitrine_db charset utf8" | mysql
echo "grant all privileges on vitrine_db.* to vitrine_user identified by '11'" | mysql
mysql vitrine_db < start_dump.sql

python manage.py runserver 127.0.0.1:8000