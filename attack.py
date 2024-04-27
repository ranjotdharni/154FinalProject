from socket import *
from urllib.request import Request, urlopen
from threading import *
from queue import *
import http.client as http, sys

concurrent = 400

def forward_request():
    forward_socket = socket(AF_INET, SOCK_STREAM)
    forward_socket.connect(('127.0.0.1', 3000))
    request = b'GET /home.html?ip=192.156.58.1 HTTP/1.1\r\n'
    forward_socket.send(request)

    # Receive the response from the other server
    response = forward_socket.recv(2048).decode()
    forward_socket.close()
    return response

def doWork():
    print("Start")
    for x in range(0, 999):
        print(f"itr is {x}")
        message = forward_request()
        print(f"{message}")

threads = []
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
    threads.append(t)

for t in threads:
    t.join()