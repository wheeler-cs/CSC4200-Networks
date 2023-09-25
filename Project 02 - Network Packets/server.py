import socket
import struct

from math import ceil

# Constants for program-wide usage
# Header Info
MIN_HEADER_SIZE = 5

# Network Transmission Info
CONN_TRANS_SIZE = 2048

# Service Types
ST_INT = 1
ST_FLOAT = 2
ST_STR = 3


def unpack_packet(conn: socket.socket, header_format: str) -> (str, str):
    # Receive first portion of packet
    client_packet = conn.recv (CONN_TRANS_SIZE)
    # Unpack packet and store header info
    ver, h_len, s_type, p_len = struct.unpack (header_format, client_packet[:5])
    packet_header_str: str = ("Version: " + str (int.from_bytes (ver, "big")) +
                              "\nHeader Len: " + str (int.from_bytes (h_len, "big")) +
                              "\nService Type: " + str (int.from_bytes (s_type, "big")) +
                              "\nPayload Length: " + str (p_len))
    h_len = int.from_bytes (h_len, "big")
    # TODO: Adjust how to read info from connection based on payload service type
    # Analyze header for how much of payload remains and receive it
    payload_str = client_packet[(h_len):].decode ("utf-8")
    receive_rounds = ceil ((p_len - (CONN_TRANS_SIZE - MIN_HEADER_SIZE)) / CONN_TRANS_SIZE)
    for count in range (0, receive_rounds):
        temp_payload = conn.recv (CONN_TRANS_SIZE)
        payload_str = payload_str + temp_payload
    # return the string - this will be the payload
    return (packet_header_str, payload_str)


if __name__ == '__main__':
    host = 'localhost'
    port = 12345

    # Fixed length header -> Version (1 byte), Header Length (1 byte), Service Type (1 byte), Payload Length (2 bytes)
    header_format = "!ccch"

    print ("[Packet Server Started]")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by: {addr}")
            while True:
                try:
                    packet_header, payload_string = unpack_packet (conn, header_format)
                    if (packet_header is not None):
                        print (packet_header)
                        print ("Payload Received:\n" + (payload_string))
                except ConnectionError as ce:
                    print (ce)
                    print ("Client disconnected")
                except Exception as e:
                    print (e)
                    print("Connection closed or an error occurred")
                    break

             #TODO: create header

             #TODO: add payload

             #TODO: send to client

