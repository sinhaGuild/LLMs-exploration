# We're using a packaged container image as opposed to installing all packages

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
