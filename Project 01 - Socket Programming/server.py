import socket

from math import ceil


LOCALHOST = "127.0.0.1"
BROADCAST_ADDRESS = LOCALHOST
PORT = 21250
CONN_QUEUE_SIZE = 5
PACKET_SIZE = 1024


# Create a socket object
connection_socket = socket.socket()

# Define the server address and port
server_address = BROADCAST_ADDRESS
server_port = PORT

# Bind the socket to the server address
connection_socket.bind ((server_address, server_port))

# Listen for incoming connections (max 5 clients in the queue)
connection_socket.listen (CONN_QUEUE_SIZE)

print("< Server is listening on port", server_port, '>')

while True:
    # Wait for a client to connect
    connection, client_address = connection_socket.accept()
    
    # Print a message to indicate the client connection
    print ("< Connection established with", client_address[0], '>')

    # Handle client data
    while True:
        # Receive data from the client
        try:
            message: str = ""       # Message from client
            message_len: int = 0    # Length of message from client
            # Receive message header and parse for arguments
            packet_header = connection.recv (PACKET_SIZE).decode ("utf-8")
            packet_args = packet_header.split (' ')
            for arg in enumerate (packet_args):
                if (arg[1] == "m_size"): # m_size: Length of message (in chars)
                    message_len = int(packet_args[arg[0] + 1])
                elif (arg[1] == "dc"): # dc: Client disconnect
                    print ('<', client_address[0], "disconnected >")
                    break
            # Get packets and reconstruct message
            # Use ceiling function to determine how many packets have been buffered
            for packets in range (0, (ceil(message_len / PACKET_SIZE))):
                packet = connection.recv (PACKET_SIZE)
                message += packet.decode ("utf-8")
            
        except ConnectionResetError: # Client disconnected w/o notifying server
            print (str(client_address[0]), "disconnected without warning")
            break
        except Exception: # Generic error when trying to read message
            print ("Unable to receive data from", str(client_address[0]))
            break

        # Send the response back to the client
        try:
            connection.sendall (message.encode ("utf-8"))
        except Exception:
            print ("Unable to echo message back to", str(client_address[0]))
            break

    # Close the client socket
    connection.shutdown (socket.SHUT_RDWR)
    connection.close()
