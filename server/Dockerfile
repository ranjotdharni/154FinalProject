FROM python:3.11

WORKDIR /server

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "-u", "server.py" ]