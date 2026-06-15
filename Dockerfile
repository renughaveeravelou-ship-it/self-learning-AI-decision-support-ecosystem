FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirment.txt .
RUN pip install --no-cache-dir -r requirment.txt

COPY . .

EXPOSE 8501
EXPOSE 8000

CMD ["streamlit", "run", "dashboard/dashboard3.py", "--server.port=8501", "--server.address=0.0.0.0"]
