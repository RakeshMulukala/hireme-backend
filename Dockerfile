FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libpq-dev netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x wait-for-db.sh

CMD ["./wait-for-db.sh", "dpg-d15fo2nfte5s739612b0-a", "5432", "uvicorn", "hiremebackend.main:app", "--host", "0.0.0.0", "--port", "8000"]
