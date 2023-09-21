
import argparse
import socket
import struct

def create_packet(version, header_length, service_type, payload):
    # TODO: Implement packet creation based on parameters
    # TODO: use the python struct module to create a fixed length header
    # TODO: Fixed length header -> Version (1 byte), Header Length (1 byte), Service Type (1 byte), Payload Length (2 bytes)
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

    #TODO: connect to the server

    #TODO: send the packet

    #TODO: recive the packet 
    
    #TODO: prints header     
    
    #TODO: prints payload
