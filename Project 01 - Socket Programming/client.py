import socket

from math import ceil

LOCALHOST = "127.0.0.1"
HOST = LOCALHOST
PORT = 21250
PACKET_SIZE = 1024

# Create a socket object
connection = socket.socket()

# Define the server address and port
server_address = HOST
server_port = PORT

# Connect to the server
try:
    connection.connect((server_address, server_port))
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
        # Send header with message metadata
        header_size = -1
        if message == "exit":
            header_size = 0
        else:
            header_size = len (message)
        message_header = "m_size " + str (header_size)
        connection.sendall (message_header.encode ("utf-8"))
        
        # Send message to server
        if message != "exit":
            s_message = ""
            connection.sendall (message.encode ("utf-8")) # Encode w/ UTF-8 to send message as binary

            # Get length of the message server is sending
            s_header = connection.recv (PACKET_SIZE)
            header_args = s_header.split (' ')
            for arg in enumerate (header_args):
                if (arg[1] == "m_size"):
                    s_message_len = int (header_args[arg[0] + 1])
            for packets in range (0, (ceil (s_message_len / PACKET_SIZE))):
                s_packet = connection.recv (PACKET_SIZE)
                s_message += s_packet.decode ("utf-8")
            
            print ("Server responded with: ")
            print (s_message)

    except Exception as e:
        break


# Close the client socket
connection.shutdown(socket.SHUT_RDWR) # Prevent additional sending and receiving of data
connection.close()
