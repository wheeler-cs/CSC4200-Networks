import socket
from math import ceil

HOST = "127.0.0.1"
PORT = 9999
PACKET_SIZE = 1024

# Create a socket object
conn_socket = socket.socket()

# Define the server address and port
server_address = HOST
server_port = PORT

# Connect to the server
try:
    conn_socket.connect((server_address, server_port))
except Exception:
    print ("Unable to connect to", HOST)
    exit (1)

while True:
    # Get user input
    message = input("Enter a message to send to the server (or 'exit' to quit): ")

    # Send the message to the server
    try:
        # Create header to send to server
        header = "header msg_size " + str (len (message))
        conn_socket.sendall (header.encode ("utf-8"))
        conn_socket.sendall (message.encode ("utf-8"))
    except Exception:
        print ("Unable to send message to server")
        break

    if (message == "exit"): # Stop client if "exit" was indicated
        break

    # Receive and print the server's response
    try:
        echo = ""
        # Receive header from client
        bin_header = conn_socket.recv (PACKET_SIZE)
        if not bin_header:
            break
        echo_header = bin_header.decode ("utf-8")
        echo_size = 0
        # Ensure "header" is first field and get message size
        parsed_header = echo_header.split (' ')
        if parsed_header[0] != "header": # First field has "header"
            break
        for i in enumerate (parsed_header): # Look for parameters (for loop for expandability)
            if i[1] == "msg_size":
                echo_size = int (parsed_header[i[0] + 1])
        if (echo_size <= 0): # Disconnect if message was empty
            break
        # Reconstruct message from individual packets
        recv_rounds = ceil (echo_size / PACKET_SIZE)
        for round in range (0, recv_rounds):
            packet = conn_socket.recv (PACKET_SIZE)
            echo += packet.decode ("utf-8")
        print ("Server echoed:")
        print (echo)
        print ("MSG SIZE:", len(echo))
    except Exception:
        print ("Couldn't receive echo from server")
        break

# Close the client socket
conn_socket.close()
