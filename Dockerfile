FROM python:3.11

COPY requirements.txt requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1 # Not leaving any pycache
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt

EXPOSE 80

COPY . /app

WORKDIR /app

CMD [ "uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--reload" ]