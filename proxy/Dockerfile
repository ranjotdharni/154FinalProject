FROM python:3.11

WORKDIR /proxy

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "-u", "proxy.py" ]