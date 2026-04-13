FROM postgres:18-alpine
WORKDIR /docker-entrypoint-initdb.d
COPY 01-init_database.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
CMD ["postgres"]