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
try:
    server_socket.connect((server_address, server_port))
except Exception as e:
    # Any interruption to connection process terminates program for safety
    print ("Unable to establish connection with server", server_address + ':' + str(server_port))
    print (f"Reason: {e}")
    exit (1)

while True:
    # Get user input
    message = input("Enter a message to send to the server (or 'exit' to quit): ")
    if not message: # Do not send an empty message
        continue

    # Send the message to the server
    try:
        if message == "exit":
            message_header = "dc"
        else:
            message_header = "m_size " + str (len (message))
        server_socket.sendall (message_header.encode ("utf-8"))
        server_socket.sendall (message.encode ("utf-8")) # Encode w/ UTF-8 to send message as binary
    except Exception:
        print ("Server at", server_address, "is currently unreachable")
        break

    # Receive and print the server's response
    try:
        server_message = (server_socket.recv (1024)).decode ("utf-8")
    except Exception:
        print ("Unable to receive data from server")
        break
    # BUG: When receiving large amounts of data, message is buffered causing queue to back up.
    print (f"Response: {server_message}")

# Close the client socket
server_socket.shutdown(socket.SHUT_RDWR) # Prevent additional sending and receiving of data
server_socket.close()
