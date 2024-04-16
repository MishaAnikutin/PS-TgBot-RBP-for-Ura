FROM python:3.11

WORKDIR /app

COPY . .
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "-m", "src.main"]
