import socket

from math import ceil

# === Constants ====================================================================================

LOCALHOST = "127.0.0.1"
HOST = LOCALHOST
PORT = 21250
PACKET_SIZE = 2048


# === Function Definitions =========================================================================

def establish_conn (target_host: str = "127.0.0.1", host_port: int = 9999) -> socket.socket:
    # Create a socket object
    new_socket = socket.socket()
    try:
        # Connect to the server
        new_socket.connect (target_host, host_port)
    except Exception:
        return None

def create_header (text: str) -> str:
    if (text == "") or (text == "exit") or (text is None):
        return "m_size 0"
    else:
        return ("m_size " + len (text))

def encode_text (text: str):
    return (text.encode ("utf-8"))

def decode_text (text) -> str:
    return (text.decode ("utf-8"))
    
def forward_message (message: str, destination: socket.socket) -> bool:
    header = create_header (message)
    if (header == "m_size 0"):
        return False
    else:
        send_rounds = ceil (len (message) / PACKET_SIZE)
        try:
            destination.send (encode_text (header))
            for r in range (0, send_rounds):
                destination.send ()
        except Exception as e:
            return False

def echo_client (conn: socket.socket) -> None:
    while True:
        # Get user input
        message = input("Enter a message to send to the server (or 'exit' to quit): ")
        # Send the message to the server
        forward_message (message, conn)
        # Receive and print the server's response


# === Main =========================================================================================

if __name__ == "__main__":
    s_connection = establish_conn (HOST, PORT)
    if (s_connection is not None):
        echo_client (s_connection)
        # Close the client socket
        s_connection.shutdown(socket.SHUT_RDWR) # Stop all incoming and outgoing transfers
        s_connection.close()
    else:
        print ("Was unable to connect to", HOST, "on port", str (PORT))
