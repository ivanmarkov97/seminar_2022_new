# https://testdriven.io/blog/docker-best-practices/

FROM python:3.9-slim

WORKDIR app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install --no-cache -r requirements.txt

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:8081", "--workers=2", "--worker-tmp-dir=/dev/shm", "app:app"]
