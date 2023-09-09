import socket

from math import ceil


LOCALHOST = "127.0.0.1"
BROADCAST_ADDRESS = LOCALHOST
PORT = 21250
CONN_QUEUE_SIZE = 5
PACKET_SIZE = 1024


# Set up server socket
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


# Run Server
while True:
    # Wait for a client to connect
    connection, client_address = connection_socket.accept()
    # Print a message to indicate the client connection
    print ("< Connection established with", client_address[0], '>')

    # Handle client data
    while True:
        # Receive data from the client
        try:
            c_message: str = "" # Message from client
            c_message_len: int = -1 # Length of message from client
            # Receive message header and parse for arguments
            packet_header = connection.recv (PACKET_SIZE).decode ("utf-8")
            # Process and respond to the client's data
            packet_args = packet_header.split (' ')
            for arg in enumerate (packet_args):
                if (arg[1] == "m_size"): # m_size: Length of message (in chars)
                    c_message_len = int (packet_args[arg[0] + 1])

            # Handles BOTH the client disconnecting normally and a dropped connection (such as client CTRL+C)
            if (c_message_len <= 0):
                print ("< Client", client_address[0], "disconnected >")
                break
            else:
                # Get packets and reconstruct message
                # Use ceiling function to determine how many packets have been buffered
                for packets in range (0, (ceil (c_message_len / PACKET_SIZE))):
                    packet = connection.recv (PACKET_SIZE)
                    c_message += packet.decode ("utf-8")
                
                print (client_address[0], ':', client_address[1],"sent", c_message)

                # Send the response back to the client
                c_header = "m_size" + str (len (c_message))
                connection.sendall (c_header)
                connection.sendall (c_message.encode ("utf-8"))
            
        except Exception: # Generic error when trying to read message
            print ("! Cannot communicate with", str(client_address[0]), '!')
            break

    # Close the client socket
    connection.shutdown (socket.SHUT_RDWR)
    connection.close()
