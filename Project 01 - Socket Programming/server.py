import socket

from math import ceil

# === Constants ====================================================================================

LOCALHOST = "127.0.0.1"
HOST = LOCALHOST
PORT = 21250
CONN_QUEUE_SIZE = 5
PACKET_SIZE = 2048


# === Function Definitions =========================================================================

def open_socket (target_ip: str = "127.0.0.1", listen_port: int = 9999):
    # Create a socket object
    new_socket = socket.socket()
    # Bind the socket to the server address
    new_socket.bind ((target_ip, listen_port))
    # Listen for incoming connections (max 5 clients in the queue)
    new_socket.listen (CONN_QUEUE_SIZE)
    print ("Server is listening on", target_ip)
    return new_socket

def get_connection (listen_socket: socket.socket) -> None:
    unused_conn_info, addr_port = listen_socket.accept()
    print (addr_port[0], "connected")

def create_header (text: str) -> str:
    if (text == "") or (text == "exit") or (text is None):
        return "m_size 0"
    else:
        return ("m_size " + str (len (text)))

def encode_text (text: str):
    return (text.encode ("utf-8"))

def decode_text (text) -> str:
    return (text.decode ("utf-8"))

def get_message_size (header: str) -> int:
    metadata = header.split (' ')
    for i in enumerate (metadata):
        if (i[0] == "m_size"):
            return int (metadata[i[0] + 1])

def receive_message (source: socket.socket) -> str:
    try:
        header = decode_text (source.recv (PACKET_SIZE))
    except Exception:
        return None
    message_size = get_message_size (header)
    receive_rounds = ceil (message_size / PACKET_SIZE)
    try:
        message = ""
        for r in range (0, receive_rounds):
            message += decode_text (source.recv (PACKET_SIZE))
    except Exception:
        return None
    return message

def echo_message (message: str, echo_destination: socket.socket) -> bool:
    header = create_header (message)
    try:
        echo_destination.sendall (encode_text (header))
        echo_destination.sendall (encode_text (message))
    except Exception:
        return False

def echo_server (c_conn: socket.socket) -> None:
    # Handle client data
    while True:
        try:
            # Receive data from the client
            message = receive_message (c_conn)
            # Process and respond to the client's data
            # Send the response back to the client
            if (message is not None):
                echo_message (message, c_conn)
            else:
                break
        except Exception:
            break


# === Main =========================================================================================

if __name__ == "__main__":
    c_connection = open_socket (HOST, PORT)
    while True:
        get_connection (c_connection)
        echo_server (c_connection)
