FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y netcat \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY requirements.txt /requirements/
RUN pip install --no-cache-dir -r /requirements/requirements.txt \
    && rm -rf /requirements

COPY ./start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start


COPY --chown=django:django . /app


USER django

WORKDIR /app

EXPOSE 9000
