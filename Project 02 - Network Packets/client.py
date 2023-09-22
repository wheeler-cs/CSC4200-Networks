
import argparse
import socket
import struct


def create_packet (version: int, header_length: int, service_type: int, payload: str) -> struct:
    print (len (payload))
    # TODO: use the python struct module to create a fixed length header
    # Packet Schema:
    #    Version        (1 byte)
    #    Header Length  (1 byte)
    #    Service Type   (1 byte)
    #    Payload Length (2 bytes)
    #    Padding        (n bytes)
    encode_str = "BBBh"
    while (len (encode_str) < header_length): # Pad to get header to expected size
        encode_str = encode_str + 'x'
    packet = struct.pack (encode_str, version, header_length, service_type, len (payload)) # TODO: change len(payload) based on data being sent
    # TODO: payload -> variable length
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

    # TODO: Create and send packet using the create_packet function
    packet = create_packet(args.version, args.header_length, args.service_type, args.payload)

    # Connect to server
    try: # Attempt socket creation and connecting to given host
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
