# Import socket library
from socket import *

# Import sys package if you want to terminate the program
import os

def create_server_socket(port):
    # Prepare a sever socket
    # Fill in start
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(1)
    # Fill in end
    print(f"The Firewall is ready to receive on port: {port}...")
    return serverSocket

def handle_request(connectionSocket):
    try:
        # Receive the HTTP request
        message = connectionSocket.recv(2048).decode()
        print("Here in Firewall")
        print(message)
        
        # Please fill in Chatgpt code here below
        target_host = "localhost"
        target_port = 12000
        target_path = "/" + message.split()[1][1:]  # You can specify a different path if needed
        firewall_signature = f"X-Firewall-Signature: {os.getenv('FIREWALL_SIGNATURE')}\r\n"
        
        # Construct the redirect URL
        redirect_url = f"Location: http://{target_host}:{target_port}{target_path}\r\n"
        
        # Construct the redirect response with 302 Found status code
        redirect_response = f"HTTP/1.1 302 Found\r\n{redirect_url}{firewall_signature}\r\n"
        
        # Send the redirect response to the client
        connectionSocket.sendall(redirect_response.encode())
        
        # Close the socket
        connectionSocket.close()
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

            <body><h1>Error 404: Page Not Found</h1></body>
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
        print("#Firewall Conn Closed#")


if __name__ == "__main__":
    port = 3000
    serverSocket = create_server_socket(port)
    while True:
        connectionSocket, addr = serverSocket.accept()
        handle_request(connectionSocket)