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

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /international

COPY --chown=intuser:intuser . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=0
ENV SECRET_KEY=django-insecure-$a8g)o$%*wi=ds%o#j459cao$(9l3%mmm2*t2+o+lb+n*(a9!)

USER intuser

RUN python ./manage.py migrate && \
    python ./manage.py collectstatic

EXPOSE 8000

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "international.wsgi:application"  ]

