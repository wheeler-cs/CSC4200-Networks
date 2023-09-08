import socket

LOCALHOST = "127.0.0.1"
BROADCAST_ADDRESS = LOCALHOST
PORT = 21250

# Create a socket object
connection_socket = socket.socket()

# Define the server address and port
server_address = BROADCAST_ADDRESS
server_port = PORT

# Bind the socket to the server address
connection_socket.bind ((server_address, server_port))

# Listen for incoming connections (max 5 clients in the queue)
connection_socket.listen()

print("Server is listening on port", server_port)

while True:
    # Wait for a client to connect
    connection, client_address = connection_socket.accept()
    
    # Print a message to indicate the client connection
    print ("Connection established with", client_address[0])

    # Handle client data
    while True:
        # Receive data from the client
        data_sent = connection.recv (1024)
        print (data_sent)
        
        # Process and respond to the client's data
        # Replace the following line with your data processing logic
        
        # Send the response back to the client
        # Replace the following line with code to send back the same message

    # Close the client socket
    # Replace the following line with code to close the client socket
