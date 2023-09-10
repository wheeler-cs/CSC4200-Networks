import socket

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
        conn_socket.sendall (message.encode ("utf-8"))
    except Exception:
        print ("Unable to send message to server")

    if (message == "exit"): # Stop client if "exit" was indicated
        break

    # Receive and print the server's response
    try:
        packet = conn_socket.recv (PACKET_SIZE)
        if not packet:
            break
        message = packet.decode ("utf-8")
        print (message)
    except Exception:
        print ("Couldn't receive echo from server")
        break

# Close the client socket
conn_socket.close()
