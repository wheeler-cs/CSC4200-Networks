import socket
import struct

def unpack_packet(conn, header_format):
    # TODO: Implement header unpacking based on received bytes
    # TODO: Create a string from the header fields
    # return the string - this will be the payload
    return packet_header_as_string

if __name__ == '__main__':
    host = 'localhost'
    port = 12345

    # Fixed length header -> Version (1 byte), Header Length (1 byte), Service Type (1 byte), Payload Length (2 bytes)
    header_format = ''  # TODO: Specify the header format using "struct"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by: {addr}")
            while True:
                try:
                    # TODO: Receive and unpack packet using the unpack_packet function
                    payload_string = unpack_packet(conn, header_format)
                    pass
                except:
                    print("Connection closed or an error occurred")
                    break

             #TODO: create header

             #TODO: add payload

             #TODO: send to client

