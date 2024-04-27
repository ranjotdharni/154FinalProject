# Import socket library
from socket import *

# Import sys package if you want to terminate the program
import os
import redis

# redirect_response = f"HTTP/1.1 302 Found\r\nLocation: http://{os.getenv('PROXY_LOCATION')}\r\nReferer: {os.getenv('FIREWALL_LOCATION')}\r\n"       

keydb_connection = redis.Redis(host=os.getenv("DB_LOCATION").split(":")[0], port=int(os.getenv("DB_LOCATION").split(":")[1]), db=0)
forward, forwardport = os.getenv("SERVER_LOCATION").split(":")
fport = int(forwardport)

errorHeaders = "HTTP/1.1 404 Not Found\r\n" + "Content-Type: text/html\r\n\r\n"
        # Fill in end

        # Prepare the HTML body content of 404 Not Found page
        # Fill in start
errorPage = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error 404</title>
    </head>

    <body><h1 style="color: red;">!!!!!!!!!!!!!!!!!<---------FIREWALL--------->!!!!!!!!!!!!!!!!!</h1></body>
    </html>
"""

err = (errorHeaders.encode() + errorPage.encode())

def create_server_socket(port):
    # Prepare a sever socket
    # Fill in start
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(1)
    # Fill in end
    print(f"The Firewall is ready to receive on port: {port}...")
    return serverSocket

def forward_request(request):
    # Forward the request to another server
    forward_socket = socket(AF_INET, SOCK_STREAM)
    forward_socket.connect((forward, fport))
    forward_socket.sendall(request)

    # Receive the response from the other server
    response = forward_socket.recv(2048).decode()
    forward_socket.close()
    return response

def handle_request(connectionSocket):
    try:
        # Receive the HTTP request
        message = connectionSocket.recv(2048).decode()
        print("Here in Firewall")

        if ("=" not in message):
            raise IOError('Cancel Request')

        cip = message.split('=')[1].split()[0]
        print(f"Getting Address {cip}...")
        check = keydb_connection.get(cip)
        if (check is None): 
            keydb_connection.set(cip, 1) 
        else:
            check = int(check)
        print(f"Got: {check}")

        if check == -1:
            connectionSocket.send(err)
            connectionSocket.close()
            return
        elif check is None:
            keydb_connection.set(cip, 1)
        elif check < 10:
            keydb_connection.set(cip, check + 1)
        else:
            keydb_connection.set(cip, -1)
            connectionSocket.send(err)
            connectionSocket.close()
            return

        response = forward_request(message.encode())
        connectionSocket.sendall(response.encode())
        connectionSocket.close()
        return
    except IOError:
        connectionSocket.send(err)
        connectionSocket.close()
        print("#Firewall Conn Closed#")


if __name__ == "__main__":
    port = 3000
    serverSocket = create_server_socket(port)
    while True:
        connectionSocket, addr = serverSocket.accept()
        handle_request(connectionSocket)