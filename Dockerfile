FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' run.sh && chmod +x run.sh

RUN python apply_fix.py

EXPOSE 8010

ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8010

CMD ["agentbeats", "run_ctrl"]
