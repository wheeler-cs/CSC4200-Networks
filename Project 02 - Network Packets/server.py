import socket
import struct

from math import ceil

# Constants for program-wide usage
# Header Info
MIN_HEADER_SIZE = 5

# Network Transmission Info
CONN_TRANS_SIZE = 512

# Service Types
ST_INT = 1
ST_FLOAT = 2
ST_STR = 3


def unpack_packet(conn: socket.socket, header_format: str):
    # Receive first portion of packet
    client_packet = conn.recv (CONN_TRANS_SIZE)
    # Unpack packet and store header info
    ver, h_len, s_type, p_len = struct.unpack (header_format, client_packet[:MIN_HEADER_SIZE])
    # Convert bin data to integers
    ver = int.from_bytes (ver, "big")
    h_len = int.from_bytes (h_len, "big")
    s_type = int.from_bytes (s_type, "big")
    # Create header as dictionary
    packet_header = {"version": ver,
                     "h_length": h_len,
                     "service": s_type,
                     "p_length": p_len}

    # Get part of payload that was received w/ header
    raw_payload = client_packet[(h_len):]
    payload = None

    # Figure out how much data is extracted due to service type
    if (s_type == ST_INT):
        payload = int.from_bytes (raw_payload, "big")
    elif (s_type == ST_FLOAT):
        payload = struct.unpack ("!f", raw_payload)
        payload = payload[0] # Payload is a tuple, get 1st elem
    elif (s_type == ST_STR):
        payload = raw_payload.decode ("utf-8")
        # Strings can have more data than a single transfer can handle
        if (p_len > CONN_TRANS_SIZE):
            recv_rounds = ceil (((p_len - h_len) / CONN_TRANS_SIZE)) - 1
            for count in range (0, recv_rounds):
                raw_payload = conn.recv (CONN_TRANS_SIZE)
                payload = payload + (raw_payload.decode ("utf-8"))

    print ("Packet Received")
    packet_header["payload"] = payload
    # return the string - this will be the payload
    return packet_header


if __name__ == '__main__':
    if (CONN_TRANS_SIZE < MIN_HEADER_SIZE):
        print ("Size of packets received must be larger than minimum header size.")
        exit (1)

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
                    packet_header = unpack_packet (conn, header_format)
                    print ("Version:", packet_header["version"])
                    print ("Header Size:", packet_header["h_length"])
                    print ("Service Type:", packet_header["service"])
                    print ("Payload Size:", packet_header["p_length"])
                    print ("Payload:")
                    print (packet_header["payload"])
                except ConnectionError or ConnectionResetError as ce:
                    print (ce)
                    print ("Client disconnected")
                    break
                except Exception as e:
                    print (e)
                    print("Connection closed or an error occurred")
                    break


            packet = None
            # Reconstruct header from data sent by client

             #TODO: add payload

             #TODO: send to client
            try:
                conn.send (packet)
            except ConnectionError or ConnectionRefusedError:
                pass


