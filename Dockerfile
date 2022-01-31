FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install --no-cache-dir --upgrade pip -r requirements.txt

COPY . .

EXPOSE 9665
CMD [ "python3", "./app.py" ]
