import argparse
import socket
import struct


# Constants for program-wide usage
# Service Types
ST_INT   = 1
ST_FLOAT = 2
ST_STR   = 3


def create_packet (version: int, header_length: int, service_type: int, payload: str) -> struct:
    # Determine payload size based on service type
    # Service Types:
    #    1 = int    (4 bytes)
    #    2 = float  (4 bytes)
    #    3 = string (variable length)
    payload_size = 0
    if (service_type == ST_INT) or (service_type == ST_FLOAT):
        payload_size = 4
    elif (service_type == ST_STR):
        payload_size = len (payload)
    else:
        # Service type is not a valid int, throw exception
        raise ValueError ("Service type {v} is outside of expected range.".format (v = service_type))

    # Packet Schema:
    #    Version        (1 byte)
    #    Header Length  (1 byte)
    #    Service Type   (1 byte)
    #    Payload Length (2 bytes)
    #    Padding        (n* bytes)
    # * Defined by the header size specified as an argument
    # BUG: Extra bytes getting added to payload, smthn to do w/ improper data sizes
    encode_str = "BBBh"
    while (len (encode_str) < header_length): # Pad to get header to expected size
        encode_str = encode_str + 'x'
    packet = struct.pack (encode_str, version, header_length, service_type, payload_size)
    # TODO: depending on the service type, handle encoding of the different types of  payload.
    # TODO: service_type 1 = payload is int, service_type 2 = payload is float, service_type 3 = payload is string

    return packet


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Client for packet creation and sending.")
    parser.add_argument('--version', type=int, required=True, help='Packet version')
    parser.add_argument('--header_length', type=int, required=True, help='Length of the packet header')
    parser.add_argument('--service_type', type=int, required=True, help='Service type of the payload (1 for int, 2 for float, 3 for string)')
    parser.add_argument('--payload', type=str, required=True, help='Payload to be packed into the packet')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=12345, help='Server port')

    args = parser.parse_args()

    # Create a packet for transferring
    try:
        packet = create_packet(args.version, args.header_length, args.service_type, args.payload)
    except ValueError as bad_value:
        print (bad_value)
        print ("Service Types: 1 = int, 2 = float, 3 = string")
        exit(1)
    
    print (packet)
    print (len (packet))

    # Attempt socket creation and connection to given host
    try:
        client_socket = socket.socket()
        client_socket.connect ((args.host, args.port))
    except ConnectionRefusedError:
        print ("Host {h}:{p} is unreachable".format (h = args.host, p = args.port))
        exit (1)
    except:
        print ("Undefined error with host {h}:{p}".format (h = args.host, p = args.port))
        exit(1)


    #TODO: send the packet

    #TODO: recive the packet 
    
    #TODO: prints header     
    
    #TODO: prints payload
