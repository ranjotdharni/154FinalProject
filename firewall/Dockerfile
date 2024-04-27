FROM python:3.11

WORKDIR /firewall

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000

CMD [ "python", "-u", "firewall.py" ]