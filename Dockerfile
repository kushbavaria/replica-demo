ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

COPY celeb_pics /code/celeb_pics
ENV SECRET_KEY "IucbRvrQcnylpedZnF6kM5s7owE3DROxHUijIdCf8t80SsJmRN"
# Run migrations
# RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python create_superuser.py

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "djangoProject.wsgi"]
