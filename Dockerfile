FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

EXPOSE 8080

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]