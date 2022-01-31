FROM python:3.8-slim-buster

WORKDIR /app
COPY . .
RUN go get -d -v ./...
RUN go install -v ./...

RUN pip3 install --no-cache-dir --upgrade pip -r requirements.txt

EXPOSE 9665
CMD [ "python3", "./app.py" ]
