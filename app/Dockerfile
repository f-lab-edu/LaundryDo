FROM python:3.11

COPY . .

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80" "--reload"]