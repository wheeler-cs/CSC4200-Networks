import socket
import struct

# Constants for program-wide usage
# Number of bytes read from network stream
CONN_TRANS_SIZE = 2048
# Service Types
ST_INT = 1
ST_FLOAT = 2
ST_STR = 3


def unpack_packet(conn: socket.socket, header_format: str):
    client_packet = conn.recv (CONN_TRANS_SIZE)
    print (client_packet)
    # TODO: Implement header unpacking based on received bytes
    # TODO: Create a string from the header fields
    packet_header_as_string: str = ""
    # return the string - this will be the payload
    return packet_header_as_string


if __name__ == '__main__':
    host = 'localhost'
    port = 12345

    # Fixed length header -> Version (1 byte), Header Length (1 byte), Service Type (1 byte), Payload Length (2 bytes)
    header_format = "BBBh"

    print ("[Packet Server Started]")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by: {addr}")
            while True:
                try:
                    payload_string = unpack_packet(conn, header_format)
                except Exception as e:
                    print (e)
                    print("Connection closed or an error occurred")
                    break

             #TODO: create header

             #TODO: add payload

             #TODO: send to client

