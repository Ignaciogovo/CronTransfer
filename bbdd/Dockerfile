FROM mysql
MAINTAINER IgnacioGovantes ignaciogovo@gmail.com

ENV MYSQL_DATABASE CronTransfer
ENV MYSQL_USER python
ENV MYSQL_PASSWORD python
ADD init.sql /docker-entrypoint-initdb.d
