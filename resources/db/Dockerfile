FROM postgres:11

RUN apt-get -y update;
RUN apt-get -y install gnupg2 wget ca-certificates rpl pwgen gdal-bin && apt-get update

RUN apt-get -y install postgresql-11-postgis-3 \
     postgresql-11-postgis-3-scripts \
     postgis


COPY ./init_db.sql /docker-entrypoint-initdb.d/init_db.sql