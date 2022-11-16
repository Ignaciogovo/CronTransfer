FROM mysql
MAINTAINER IgnacioGovantes ignaciogovo@gmail.com

ENV MYSQL_DATABASE easybackups
ENV MYSQL_USER python
ENV MYSQL_PASSWORD python
ADD init.sql /docker-entrypoint-initdb.d

EXPOSE 3306