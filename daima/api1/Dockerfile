#  cat Dockerfile
# FROM python:3.9
# WORKDIR /code
# COPY ./requirements.txt /code/requirements.txt
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# EXPOSE 5432
# COPY ./app /code/app
# CMD ["fastapi", "run", "app/main.py", "--port", "5432"]
#  cat Dockerfile
FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 8000
COPY ./app /code/app
COPY ./main.py /code/main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]