import socket
from math import ceil

HOST = "127.0.0.1"
PORT = 9999
LISTEN_QUEUE_SIZE = 5
PACKET_SIZE = 1024

# Create a socket object
try:
    conn_socket = socket.socket()

    # Define the server address and port
    server_address = HOST
    server_port = PORT

    # Bind the socket to the server address
    conn_socket.bind ((server_address, server_port))

    # Listen for incoming connections (max 5 clients in the queue)
    conn_socket.listen (LISTEN_QUEUE_SIZE)
    print("Server is listening on", server_address)
except Exception:
    print ("Server could not be initialized due to issue with socket creation")
    exit (1)

while True:
    # Wait for a client to connect
    try:
        conn_info, addr_port = conn_socket.accept()
    except Exception:
        print ("Something went wrong when trying to accept incoming connection")
    
    # Print a message to indicate the client connection
    print ("Client", addr_port[0], "connected on port", str (addr_port[1]))

    # Handle client data
    while True:
        # Receive data from the client
        message = ""
        try:
            # Receive header from client
            bin_header = conn_info.recv (PACKET_SIZE)
            if not bin_header:
                break
            header = bin_header.decode ("utf-8")
            message_size = 0
            # Ensure "header" is first field and get message size
            parsed_header = header.split (' ')
            if parsed_header[0] != "header": # First field has "header"
                break
            for i in enumerate (parsed_header): # Look for parameters (for loop for expandability)
                if i[1] == "msg_size":
                    message_size = int (parsed_header[i[0] + 1])
            if (message_size <= 0): # Disconnect if message was empty
                break
            # Reconstruct message from individual packets
            recv_rounds = ceil (message_size / PACKET_SIZE)
            for round in range (0, recv_rounds):
                packet = conn_info.recv (PACKET_SIZE)
                message += packet.decode ("utf-8")
        except Exception:
            print ("Unable to receive message from client")
            break

        # Process and respond to the client's data
        if (len (message) > 0):
            print (addr_port[0], "sent:")
            print (message)
        if (message == "exit"):
            break
        
        # Send the response back to the client
        try:
            header = "header msg_size " + str (len (message))
            conn_info.sendall (header.encode ("utf-8"))
            conn_info.sendall (message.encode ("utf-8"))
        except Exception:
            print ("Couldn't echo message back to client")

    # Close the client socket
    print (addr_port[0], "disconnected")
    conn_info.close()