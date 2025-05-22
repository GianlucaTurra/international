FROM python:3.13-alpine3.21

RUN mkdir /international

WORKDIR /international

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt /international/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /international

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]
