import argparse
import socket
import struct


# Constants for program-wide usage
# Header Info
MIN_HEADER_LEN = 6

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
    payload_size: int = 0
    if (service_type == ST_INT) or (service_type == ST_FLOAT):
        payload_size = 4
    elif (service_type == ST_STR):
        payload_size = len (payload)
    else:
        # Service type is not a valid int, throw exception
        raise ValueError ("Service type {v} is outside of expected range.".format (v = service_type))
    
    # With the current schema (see below) header must be AT LEAST 6 bytes in length. Throw an error
    # if the size specified is below this.
    if (header_length < MIN_HEADER_LEN):
        raise ValueError ("Header size specified does not meet minimum requirements (x >= {n}).".format (n = MIN_HEADER_LEN))

    # Packet Schema:
    #    Version        (1 byte)
    #    Header Length  (1 byte)
    #    Service Type   (1 byte)
    #    Payload Length (2 bytes)
    #    Padding        (n* bytes)
    #    NULL - 0x00    (1 byte), appended by struct.pack operation
    # * Affected by the header size given to the function.
    encoder_str = "BBBh" + ('x' * ((header_length - 1) - 5))
    packet = struct.pack (encoder_str, version, header_length, service_type, payload_size)

    # TODO: depending on the service type, handle encoding of the different types of  payload.
    encoded_payload = None
    if (service_type == ST_INT):
        # BUG: Need to get actual binary data instead of a string representing the bin data.
        encoded_payload = format (int(payload), "08b")
        pass
    elif (service_type == ST_FLOAT):
        pass
    elif (service_type == ST_STR):
        # TODO: Make sure chars are 8 bits when encoded
        encoded_payload = payload.encode ("utf-8")

    # Append packet data to end of header and return whole thing
    print (encoded_payload)
    packet = packet + encoded_payload
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
        exit(1)
    
    print (packet)

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
