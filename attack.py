from urllib.request import Request, urlopen
from threading import *
from queue import *
import http.client as http, sys

concurrent = 400

def doWork():
    for x in range(0, 999):
        req = Request("http://localhost:12000/home.html")
        req.add_header('Connection', 'keep-alive')
        res = urlopen(req).read()
        print(f"{res}\n\n")

threads = []
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
    threads.append(t)

for t in threads:
    t.join()