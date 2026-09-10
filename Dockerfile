FROM python:3.13-slim-bookworm

WORKDIR /lorica-api

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .   

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]