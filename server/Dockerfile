# ignore this file for now, it's not used in the project

FROM python:3.8-slim

WORKDIR /app

COPY ../requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src ./src
EXPOSE 8000

CMD [ "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]