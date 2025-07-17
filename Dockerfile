# Builder container
FROM python:3.13-alpine3.21 AS builder

RUN mkdir /international

WORKDIR /international

RUN pip install --upgrade pip

COPY requirements.txt /international/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /international

# Actual factual container
FROM python:3.13-alpine3.21 

RUN adduser -D -h /home/intuser intuser && \
    mkdir /international && \
    chown -R intuser /international

RUN apk add curl && \
    curl -sfS https://dotenvx.sh/install.sh | sh && \
    dotenvx encrypt

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /international

COPY --chown=intuser:intuser . .

# ENV PYTHONDONTWRITEBYTECODE=${PYTHONDONTWRITEBYTECODE}
# ENV PYTHONUNBUFFERED=${PYTHONUNBUFFERED}
# ENV DEBUG=${DEBUG}
# ENV SECRET_KEY=${SECRET_KEY}

USER intuser

RUN dotenvx run -f .env.prod -- python ./manage.py migrate && \
    dotenvx run -f .env.prod -- python ./manage.py collectstatic

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "international.wsgi:application"  ]

