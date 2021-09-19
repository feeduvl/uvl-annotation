FROM python:3.8-slim-buster

WORKDIR /app
COPY . .

RUN pip3 install --upgrade pip -r requirements.txt

EXPOSE 9661
CMD [ "python3", "./app.py" ]