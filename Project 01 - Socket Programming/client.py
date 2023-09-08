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

while True:
    # Get user input
    message = input("Enter a message to send to the server (or 'exit' to quit): ")
        
    # Send the message to the server
    # Replace the following line with code to send the message

    # Receive and print the server's response
    # Replace the following line with code to receive and print the response
    # Make sure you are able to receive long messages

# Close the client socket
# Replace the following line with code to close the client socket
