import socket

LOCALHOST = "127.0.0.1"
BROADCAST_ADDRESS = LOCALHOST
PORT = 21250
CONN_QUEUE_SIZE = 5

# Create a socket object
connection_socket = socket.socket()

# Define the server address and port
server_address = BROADCAST_ADDRESS
server_port = PORT

# Bind the socket to the server address
connection_socket.bind ((server_address, server_port))

# Listen for incoming connections (max 5 clients in the queue)
connection_socket.listen (CONN_QUEUE_SIZE)

print("Server is listening on port", server_port)

while True:
    # Wait for a client to connect
    connection, client_address = connection_socket.accept()
    
    # Print a message to indicate the client connection
    print ("Connection established with", client_address[0])

    # Handle client data
    while True:
        # Receive data from the client
        try:
            data_sent = connection.recv (1024)
        except ConnectionResetError: # Client host disconnected w/o sending "exit"
            print (str(client_address[0]), "disconnected without signaling")
            break
        except Exception: # Generic error when trying to read message
            print ("Unable to receive data from", str(client_address[0]))
            break
        
        # Process and respond to the client's data
        message = data_sent.decode ("utf-8")
        if message == "exit": # "exit" indicates client is disconnecting
            print (str(client_address[0]), "disconnected")
            break
        elif not message:
            print (str(client_address[0]), "sent a blank message")
            continue
        else:
            print (str(client_address[0]), "Sent:", message)

        # Send the response back to the client
        try:
            connection.sendall (data_sent)
        except Exception:
            print ("Unable to echo message back to", str(client_address[0]))
            break

    # Close the client socket
    connection.shutdown (socket.SHUT_RDWR)
    connection.close()
