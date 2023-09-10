import socket

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
            packet = conn_info.recv (PACKET_SIZE)
            if not packet:
                break
            message = packet.decode ("utf-8")
        except Exception:
            print ("Unable to receive message from client")
            break

        # Process and respond to the client's data
        if (len (message) > 0):
            print (message)
        if (message == "exit"):
            break
        
        # Send the response back to the client
        try:
            conn_info.sendall (message.encode ("utf-8"))
        except Exception:
            print ("Couldn't echo message back to client")

    # Close the client socket
    print (addr_port[0], "disconnected")
    conn_info.close()