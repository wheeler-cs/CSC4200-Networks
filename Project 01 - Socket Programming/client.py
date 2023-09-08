import socket

LOCALHOST = "127.0.0.1"
HOST = LOCALHOST
PORT = 21250

# Create a socket object
server_socket = socket.socket()

# Define the server address and port
server_address = HOST
server_port = PORT

# Connect to the server
try:
    server_socket.connect((server_address, server_port))
except Exception as e:
    # Any interruption to connection process terminates program for safety
    print ("Unable to establish connection with server", server_address + ':' + str(server_port))
    print (f"Reason: {e}")
    exit(1)

while True:
    # Get user input
    message = input("Enter a message to send to the server (or 'exit' to quit): ")

    if message == "exit":
        break
    # Send the message to the server
    server_socket.sendall(message.encode ("utf-8"))
    # Receive and print the server's response
    # Replace the following line with code to receive and print the response
    # Make sure you are able to receive long messages

# Close the client socket
server_socket.shutdown()
server_socket.close()
