FROM python:3.9-alpine3.16

WORKDIR /envirotrack

RUN apk add --no-cache gettext postgresql-client build-base postgresql-dev \
    && adduser --disabled-password service-user

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY envirotrack /envirotrack

USER service-user

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# FROM python:3.9-alpine3.16

# WORKDIR /envirotrack

# RUN apk add --no-cache gettext postgresql-client build-base postgresql-dev \
#     && adduser --disabled-password service-user

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY envirotrack /envirotrack

# USER service-user

# # Устанавливаем переменные среды для конфигурации PostgreSQL
# ENV POSTGRES_DB=dbname
# ENV POSTGRES_USER=dbuser
# ENV POSTGRES_PASSWORD=pass


# RUN apk add --no-cache postgresql
# RUN echo "CREATE DATABASE $POSTGRES_DB;" | su-exec postgres psql
# RUN echo "CREATE USER $POSTGRES_USER WITH SUPERUSER PASSWORD '$POSTGRES_PASSWORD';" | su-exec postgres psql


# EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]