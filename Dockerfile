FROM python:3.10

COPY serving/requirements.txt .
RUN pip install -r requirements.txt

COPY setup.py someproject/setup.py
COPY src someproject/src
RUN pip install someproject/

COPY serving/src/fastapi_server.py server.py
COPY serving/artifact artifact

EXPOSE 8000
CMD gunicorn server:app --bind 0.0.0.0:8000 --workers 2 --worker-class uvicorn.workers.UvicornWorker
