# Import socket library
from socket import *

# Import sys package if you want to terminate the program
import sys

def create_server_socket(port):
    # Prepare a sever socket
    # Fill in start
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(1)
    # Fill in end
    print(f"The server is ready to receive on port: {port}")
    return serverSocket

def handle_request(connectionSocket):
    try:
        # Receive the HTTP request
        message = connectionSocket.recv(2048).decode()
        print("Here")
        print(message)
        # Prepare HTTP response header
        # Fill in start
        headers = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n\r\n"
        # Fill in end

        r = b'GET http://www.google.com HTTP/1.1\n\n'
        
        for i in range(0, 9):
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(('www.google.com', 80))
            s.send(r)
            print(s.recv(4096).decode())
            s.close()

        # Get the requested file from the message
        filename = message.split()[1][1:]
        # Open the requested file and get the HTML body content
        # Fill in start
        with open(filename, 'r') as temp:
            file = temp.read()
        # Fill in en

        # Send response message
        # Fill in start
        connectionSocket.send(headers.encode() + file.encode())
        # Fill in end

        # Close the socket
        # Fill in start
        connectionSocket.close()
        # Fill in end

        # Terminate the program after sending the corresponding data
        # Comment it out if you want the server to be always ON
        # sys.exit()


    except IOError:
        # Prepare 404 Not Found HTTP header
        # Fill in start
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

            <body><h1>Error 404: The requested file (""" + filename + """) was not found.</h1></body>
            </html>
        """
        # Fill in end

        # Send response message
        # Fill in start
        connectionSocket.send(errorHeaders.encode() + errorPage.encode())
        # Fill in end

        # Close socket
        # Fill in start
        connectionSocket.close()
        # Fill in end


if __name__ == "__main__":
    port = 12000
    serverSocket = create_server_socket(port)
    while True:
        connectionSocket, addr = serverSocket.accept()
        handle_request(connectionSocket)