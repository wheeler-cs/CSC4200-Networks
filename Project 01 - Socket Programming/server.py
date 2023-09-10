import socket

HOST = "127.0.0.1"
PORT = 9999
LISTEN_QUEUE_SIZE = 5

# Create a socket object
conn_socket = socket.socket()

# Define the server address and port
server_address = HOST
server_port = PORT

# Bind the socket to the server address
conn_socket.bind ((server_address, server_port))

# Listen for incoming connections (max 5 clients in the queue)
conn_socket.listen (LISTEN_QUEUE_SIZE)
print("Server is listening on", server_address)

while True:
    # Wait for a client to connect
    conn_info, addr_port = conn_socket.accept()
    
    # Print a message to indicate the client connection
    print ("Client", addr_port[0], "connected on port", str (addr_port[1]))
    break

    # Handle client data
    while True:
        pass
        # Receive data from the client
        # Replace the following line with code to receive data
        # ensure you can receive long messages
        
        
        # Process and respond to the client's data
        # Replace the following line with your data processing logic
        
        # Send the response back to the client
        # Replace the following line with code to send back the same message

    # Close the client socket
    # Replace the following line with code to close the client socket
