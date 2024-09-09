FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y python3-venv && \
    pip install pytest-playwright && \
    playwright install --with-deps chromium

WORKDIR /home/jm-autotests/

COPY . .

RUN python3 -m venv venv

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x run.sh

ENTRYPOINT ["./run.sh"]
