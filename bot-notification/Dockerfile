FROM python:3.11-slim

RUN apt install tzdata
ENV TZ=Europe/Moscow

WORKDIR app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["python", "main.py"]
