import argparse
import socket
import struct


# Constants for program-wide usage
# Header Info
MIN_HEADER_LEN = 5

# Network Transmission Info
CONN_TRANS_SIZE = 2048

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
    else: # Service type is not a valid int, throw exception
        raise ValueError ("Service type {v} is outside of expected range.".format (v = service_type))
    # With the current schema (see below) header must be AT LEAST 5 bytes in length. Throw an error
    # if the size specified is below this.
    if (header_length < MIN_HEADER_LEN):
        raise ValueError ("Header size specified does not meet minimum requirements (x >= {n}).".format (n = MIN_HEADER_LEN))
    # Packet Schema:
    # Uses big (network) endian
    #    Version        (1 byte)
    #    Header Length  (1 byte)
    #    Service Type   (1 byte)
    #    Payload Length (2 bytes)
    #    Padding        (n bytes)*
    #    Payload        (Size Varies)
    # * Affected by the header size given to the function.
    # Pad NULL values (if applicable)
    encoder_str = "!ccch" + ('x' * (header_length - 5))
    # Add service type to encoder and cast payload to proper data type
    if (service_type == ST_INT):
        encoder_str = encoder_str + 'i'
        payload = int (payload)
    elif (service_type == ST_FLOAT):
        encoder_str = encoder_str + 'f'
        payload = float (payload)
    elif (service_type == ST_STR):
        encoder_str = encoder_str + str (len (payload)) + 's'
        payload = bytes (payload, 'utf-8')
    # Pack header and payload into single binary entity
    packet = struct.pack (encoder_str, bytes ([version]), bytes ([header_length]), bytes ([service_type]), payload_size, payload)
    return packet


if __name__ == '__main__':
    # Setup command line arguments, and specify which are required
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
        exit (1)
    except Exception as unhandled_e:
        print ("While creating a packet for tranmission, an unhandled error occurred.")
        print (unhandled_e)
        exit (1)

    # Attempt socket creation and connection to given host
    try:
        client_socket = socket.socket()
        client_socket.connect ((args.host, args.port))
    except ConnectionRefusedError:
        print ("Host {h}:{p} is unreachable".format (h = args.host, p = args.port))
        client_socket.close()
        exit (1)
    except:
        print ("Undefined error with host {h}:{p}".format (h = args.host, p = args.port))
        client_socket.close()
        exit (1)

    # Send packet to remote host
    try:
        client_socket.sendall (packet)
    except ConnectionRefusedError:
        print ("Connection to remote host interrupted.")
        client_socket.close()
        exit (1)
    except ConnectionResetError:
        print ("Remote host disconnected.")
        client_socket.close()
        exit (1)
    except Exception as send_e:
        print ("Unable to send packet to remote host")
        client_socket.close()
        exit (1)

    # Receive new packet from server
    server_packet = client_socket.recv (CONN_TRANS_SIZE)
    client_socket.close() # Done w/ transmission, close socket conn
    
    # Print header of received packet
    encoder_str = "!ccch" + ('x' * (args.header_length - 5))
    if args.service_type == ST_INT:
        encoder_str = encoder_str + 'i'
    elif args.service_type == ST_FLOAT:
        encoder_str = encoder_str + 'f'
    elif args.service_type == ST_STR:
        encoder_str = encoder_str + 's'
    ver, h_len, s_type, p_len, payload = struct.unpack (encoder_str, server_packet)
    ver = int.from_bytes (ver, "big")
    h_len = int.from_bytes (h_len, "big")
    s_type = int.from_bytes (s_type, "big")
    print ("=== Returned Info ===")
    print ("Version:", ver)
    print ("Header Length:", h_len, "bytes")
    print ("Service Type:", s_type)
    print ("Payload Size:", p_len, "bytes")

    # Print payload of received packet
    print (payload)
